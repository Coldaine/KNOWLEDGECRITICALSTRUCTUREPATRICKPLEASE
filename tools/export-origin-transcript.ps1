[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$SessionPath,

    [Parameter(Mandatory)]
    [string]$CutoffTimestamp,

    [string]$OutputPath = "source/origin-conversation-verbatim.md",
    [string]$ProvenancePath = "source/provenance.md",
    [string]$ChecksumPath = "source/SHA256SUMS"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$repositoryRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))

function Resolve-OutputPath {
    param([Parameter(Mandatory)][string]$Path)

    if ([IO.Path]::IsPathRooted($Path)) {
        return [IO.Path]::GetFullPath($Path)
    }

    return [IO.Path]::GetFullPath((Join-Path $repositoryRoot $Path))
}

function ConvertFrom-SessionTimestamp {
    param([Parameter(Mandatory)][string]$Value)

    return [DateTimeOffset]::Parse(
        $Value,
        [Globalization.CultureInfo]::InvariantCulture,
        [Globalization.DateTimeStyles]::AssumeUniversal
    )
}

function Get-TextSha256 {
    param([Parameter(Mandatory)][AllowEmptyString()][string]$Text)

    $sha = [Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [Text.UTF8Encoding]::new($false).GetBytes($Text)
        return ([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace("-", "").ToLowerInvariant()
    }
    finally {
        $sha.Dispose()
    }
}

$resolvedSessionPath = (Resolve-Path -LiteralPath $SessionPath).Path
$resolvedOutputPath = Resolve-OutputPath -Path $OutputPath
$resolvedProvenancePath = Resolve-OutputPath -Path $ProvenancePath
$resolvedChecksumPath = Resolve-OutputPath -Path $ChecksumPath
$cutoff = ConvertFrom-SessionTimestamp -Value $CutoffTimestamp

$entries = [Collections.Generic.List[object]]::new()
$turnEntryIndexes = [Collections.Generic.List[object]]::new()
$currentTurnEntryIndexes = $null
$requestInputCalls = @{}
$abortedTurns = [Collections.Generic.List[object]]::new()
$rollbackEvents = [Collections.Generic.List[object]]::new()
$sessionId = $null
$lineNumber = 0

foreach ($line in Get-Content -LiteralPath $resolvedSessionPath) {
    $lineNumber++

    $timestampText = $null
    if ($line -match '"timestamp":"([^"]+)"') {
        $timestampText = $Matches[1]
        if ((ConvertFrom-SessionTimestamp -Value $timestampText) -gt $cutoff) {
            break
        }
    }

    $record = $line | ConvertFrom-Json -Depth 100

    if ($record.type -eq "session_meta") {
        $sessionId = [string]$record.payload.id
        continue
    }

    if ($record.type -eq "event_msg" -and $record.payload.type -eq "task_started") {
        $currentTurnEntryIndexes = [Collections.Generic.List[int]]::new()
        $turnEntryIndexes.Add($currentTurnEntryIndexes)
        continue
    }

    if ($record.type -eq "event_msg" -and $record.payload.type -eq "turn_aborted") {
        $abortedTurns.Add([pscustomobject]@{
            Line      = $lineNumber
            Timestamp = $timestampText
            TurnId    = [string]$record.payload.turn_id
            Reason    = [string]$record.payload.reason
        })
        continue
    }

    if ($record.type -eq "event_msg" -and $record.payload.type -eq "thread_rolled_back") {
        $numTurns = [int]$record.payload.num_turns
        if ($numTurns -lt 1 -or $numTurns -gt $turnEntryIndexes.Count) {
            throw "Invalid rollback of $numTurns turn(s) at source line $lineNumber; $($turnEntryIndexes.Count) tracked turn(s) are available."
        }

        $firstRolledBackTurn = $turnEntryIndexes.Count - $numTurns
        for ($turnIndex = $firstRolledBackTurn; $turnIndex -lt $turnEntryIndexes.Count; $turnIndex++) {
            foreach ($index in $turnEntryIndexes[$turnIndex]) {
                $entries[$index].RolledBack = $true
            }
        }

        for ($removed = 0; $removed -lt $numTurns; $removed++) {
            $turnEntryIndexes.RemoveAt($turnEntryIndexes.Count - 1)
        }

        if ($turnEntryIndexes.Count -gt 0) {
            $currentTurnEntryIndexes = $turnEntryIndexes[$turnEntryIndexes.Count - 1]
        }
        else {
            $currentTurnEntryIndexes = $null
        }
        $rollbackEvents.Add([pscustomobject]@{
            Line      = $lineNumber
            Timestamp = $timestampText
            NumTurns  = $numTurns
        })
        continue
    }

    if ($record.type -ne "response_item") {
        continue
    }

    if ($record.payload.type -eq "message" -and $record.payload.role -in @("user", "assistant")) {
        $parts = @(
            $record.payload.content |
                Where-Object { $_.type -in @("input_text", "output_text") } |
                ForEach-Object { [string]$_.text }
        )

        if ($parts.Count -eq 0) {
            throw "Message at source line $lineNumber has no text content."
        }

        $text = $parts -join "`n"
        $entry = [pscustomobject]@{
            Line       = $lineNumber
            Timestamp  = $timestampText
            Role       = if ($record.payload.role -eq "user") { "User" } else { "Assistant" }
            Kind       = "message"
            Text       = $text
            TextSha256 = Get-TextSha256 -Text $text
            RolledBack = $false
        }
        $entries.Add($entry)
        if ($null -eq $currentTurnEntryIndexes) {
            throw "Message at source line $lineNumber is not inside a tracked turn."
        }
        $currentTurnEntryIndexes.Add($entries.Count - 1)
        continue
    }

    if ($record.payload.type -eq "function_call" -and $record.payload.name -eq "request_user_input") {
        $entry = [pscustomobject]@{
            Line       = $lineNumber
            Timestamp  = $timestampText
            Role       = "Assistant"
            Kind       = "interactive prompt"
            Text       = [string]$record.payload.arguments
            TextSha256 = Get-TextSha256 -Text ([string]$record.payload.arguments)
            RolledBack = $false
        }
        $entries.Add($entry)
        if ($null -eq $currentTurnEntryIndexes) {
            throw "Interactive prompt at source line $lineNumber is not inside a tracked turn."
        }
        $currentTurnEntryIndexes.Add($entries.Count - 1)
        $requestInputCalls[[string]$record.payload.call_id] = $true
        continue
    }

    if (
        $record.payload.type -eq "function_call_output" -and
        $requestInputCalls.ContainsKey([string]$record.payload.call_id)
    ) {
        $entry = [pscustomobject]@{
            Line       = $lineNumber
            Timestamp  = $timestampText
            Role       = "User"
            Kind       = "interactive response"
            Text       = [string]$record.payload.output
            TextSha256 = Get-TextSha256 -Text ([string]$record.payload.output)
            RolledBack = $false
        }
        $entries.Add($entry)
        if ($null -eq $currentTurnEntryIndexes) {
            throw "Interactive response at source line $lineNumber is not inside a tracked turn."
        }
        $currentTurnEntryIndexes.Add($entries.Count - 1)
    }
}

if (-not $sessionId) {
    throw "The session metadata did not contain an id."
}

$canonicalEntries = @($entries | Where-Object { -not $_.RolledBack } | Sort-Object Line)
$rolledBackEntries = @($entries | Where-Object { $_.RolledBack } | Sort-Object Line)
$messageEntries = @($entries | Where-Object { $_.Kind -eq "message" })
$interactiveEntries = @($entries | Where-Object { $_.Kind -ne "message" })

$transcript = [Text.StringBuilder]::new()
[void]$transcript.Append("# Origin conversation - verbatim`n`n")
[void]$transcript.Append("This is the complete canonical human/assistant conversation captured from the original Codex session through the recorded cutoff. Message bodies are unchanged. Headings and timestamps are the only additions.`n`n")
[void]$transcript.Append("- Session: ``$sessionId```n")
[void]$transcript.Append("- Cutoff: ``$CutoffTimestamp```n")
[void]$transcript.Append("- Canonical entries: $($canonicalEntries.Count)`n")
[void]$transcript.Append("- Extraction details: [provenance.md](provenance.md)`n`n")

$sequence = 0
foreach ($entry in $canonicalEntries) {
    $sequence++
    $anchor = "T{0:D3}" -f $sequence
    $kindSuffix = if ($entry.Kind -eq "message") { "" } else { " - $($entry.Kind)" }
    [void]$transcript.Append("## $anchor - $($entry.Role)$kindSuffix`n`n")
    [void]$transcript.Append("``$($entry.Timestamp)```n`n")

    if ($entry.Kind -eq "message") {
        [void]$transcript.Append($entry.Text)
        if (-not $entry.Text.EndsWith("`n")) {
            [void]$transcript.Append("`n")
        }
    }
    else {
        [void]$transcript.Append("~~~json`n")
        [void]$transcript.Append($entry.Text)
        if (-not $entry.Text.EndsWith("`n")) {
            [void]$transcript.Append("`n")
        }
        [void]$transcript.Append("~~~`n")
    }
    [void]$transcript.Append("`n")
}

$utf8NoBom = [Text.UTF8Encoding]::new($false)
$transcriptText = $transcript.ToString()
[IO.File]::WriteAllText($resolvedOutputPath, $transcriptText, $utf8NoBom)

$provenance = [Text.StringBuilder]::new()
[void]$provenance.AppendLine("# Transcript provenance")
[void]$provenance.AppendLine()
[void]$provenance.AppendLine("## Source")
[void]$provenance.AppendLine()
[void]$provenance.AppendLine("- Session ID: ``$sessionId``")
[void]$provenance.AppendLine("- Source file: ``$([IO.Path]::GetFileName($resolvedSessionPath))``")
[void]$provenance.AppendLine("- Cutoff timestamp: ``$CutoffTimestamp``")
[void]$provenance.AppendLine("- Raw user/assistant message records through cutoff: $($messageEntries.Count)")
[void]$provenance.AppendLine("- Rolled-back conversation entries excluded from the canonical conversation: $($rolledBackEntries.Count)")
[void]$provenance.AppendLine("- Interactive prompt/response records included: $($interactiveEntries.Count)")
[void]$provenance.AppendLine("- Canonical transcript entries: $($canonicalEntries.Count)")
[void]$provenance.AppendLine()
[void]$provenance.AppendLine("## Inclusion rules")
[void]$provenance.AppendLine()
[void]$provenance.AppendLine("- Include every ``response_item`` message whose role is ``user`` or ``assistant``.")
[void]$provenance.AppendLine("- Include ``request_user_input`` prompts and their matching user responses because they contain visible conversation decisions.")
[void]$provenance.AppendLine("- Preserve message text exactly as stored. Add only transcript headings and timestamps.")
[void]$provenance.AppendLine("- When one message record contains several text parts, concatenate those parts in source order with one LF; the transcript does not otherwise mark the part boundary.")
[void]$provenance.AppendLine("- Generate transcript framing with LF while preserving any line-ending characters inside source message bodies; the transcript is marked non-normalizing in ``.gitattributes``.")
[void]$provenance.AppendLine("- Exclude entries belonging to a turn that the session records as rolled back.")
[void]$provenance.AppendLine()
[void]$provenance.AppendLine("## Exclusions")
[void]$provenance.AppendLine()
[void]$provenance.AppendLine("- System and developer instructions")
[void]$provenance.AppendLine("- Hidden reasoning")
[void]$provenance.AppendLine("- Ordinary shell, web, and collaboration tool calls and outputs")
[void]$provenance.AppendLine("- Subagent traffic")
[void]$provenance.AppendLine("- Event-stream bookkeeping other than rollback evidence")
[void]$provenance.AppendLine()
[void]$provenance.AppendLine("These records are implementation plumbing rather than human/assistant conversation. The interactive questionnaire is the exception because the user supplied decisions through it.")
[void]$provenance.AppendLine()
[void]$provenance.AppendLine("## Rollback and replay evidence")
[void]$provenance.AppendLine()

if ($rolledBackEntries.Count -eq 0) {
    [void]$provenance.AppendLine("No rolled-back conversation entries occurred before the cutoff.")
}
else {
    foreach ($entry in $rolledBackEntries) {
        $replay = $canonicalEntries |
            Where-Object {
                $_.Line -gt $entry.Line -and
                $_.Role -eq $entry.Role -and
                $_.Kind -eq $entry.Kind -and
                $_.TextSha256 -eq $entry.TextSha256
            } |
            Select-Object -First 1

        $replayText = if ($replay) { "; replayed at source line $($replay.Line)" } else { "; no identical replay found" }
        [void]$provenance.AppendLine("- Source line $($entry.Line), $($entry.Role), SHA-256 ``$($entry.TextSha256)``$replayText.")
    }

    foreach ($turn in $abortedTurns) {
        [void]$provenance.AppendLine("- Turn ``$($turn.TurnId)`` was aborted as ``$($turn.Reason)`` at source line $($turn.Line).")
    }

    foreach ($rollback in $rollbackEvents) {
        [void]$provenance.AppendLine("- ``thread_rolled_back`` removed $($rollback.NumTurns) turn(s) at source line $($rollback.Line).")
    }
}

[void]$provenance.AppendLine()
[void]$provenance.AppendLine("Each rolled-back duplicate is omitted once from the canonical transcript because the event stream proves that its first turn was rolled back before the same user content was replayed. The underlying text and both source locations remain auditable here.")
[void]$provenance.AppendLine()
[void]$provenance.AppendLine("## Reproduction")
[void]$provenance.AppendLine()
[void]$provenance.AppendLine("Run from the repository root:")
[void]$provenance.AppendLine()
[void]$provenance.AppendLine('~~~powershell')
[void]$provenance.AppendLine("./tools/export-origin-transcript.ps1 ``")
[void]$provenance.AppendLine("  -SessionPath '<path-to-session-jsonl>' ``")
[void]$provenance.AppendLine("  -CutoffTimestamp '$CutoffTimestamp'")
[void]$provenance.AppendLine('~~~')

$provenanceText = $provenance.ToString().Replace("`r`n", "`n")
[IO.File]::WriteAllText($resolvedProvenancePath, $provenanceText, $utf8NoBom)

$outputRelative = [IO.Path]::GetRelativePath($repositoryRoot, $resolvedOutputPath).Replace("\", "/")
$provenanceRelative = [IO.Path]::GetRelativePath($repositoryRoot, $resolvedProvenancePath).Replace("\", "/")
$outputHash = (Get-FileHash -LiteralPath $resolvedOutputPath -Algorithm SHA256).Hash.ToLowerInvariant()
$provenanceHash = (Get-FileHash -LiteralPath $resolvedProvenancePath -Algorithm SHA256).Hash.ToLowerInvariant()
$checksumText = "$outputHash  $outputRelative`n$provenanceHash  $provenanceRelative`n"
[IO.File]::WriteAllText($resolvedChecksumPath, $checksumText, $utf8NoBom)

[pscustomobject]@{
    session_id                 = $sessionId
    cutoff                     = $CutoffTimestamp
    raw_message_records        = $messageEntries.Count
    rolled_back_records        = $rolledBackEntries.Count
    interactive_records        = $interactiveEntries.Count
    canonical_transcript_items = $canonicalEntries.Count
    transcript_path            = $outputRelative
    transcript_sha256          = $outputHash
    provenance_path            = $provenanceRelative
    provenance_sha256          = $provenanceHash
} | ConvertTo-Json
