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

function Resolve-OutputPath {
    param([Parameter(Mandatory)][string]$Path)

    if ([IO.Path]::IsPathRooted($Path)) {
        return [IO.Path]::GetFullPath($Path)
    }

    return [IO.Path]::GetFullPath((Join-Path (Get-Location) $Path))
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
$repositoryRoot = [IO.Path]::GetFullPath((Get-Location).Path)
$cutoff = [DateTimeOffset]::Parse(
    $CutoffTimestamp,
    [Globalization.CultureInfo]::InvariantCulture,
    [Globalization.DateTimeStyles]::AssumeUniversal
)

$entries = [Collections.Generic.List[object]]::new()
$currentTurnEntryIndexes = [Collections.Generic.List[int]]::new()
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
        if ([DateTimeOffset]::Parse($timestampText) -gt $cutoff) {
            break
        }
    }

    $record = $line | ConvertFrom-Json -Depth 100

    if ($record.type -eq "session_meta") {
        $sessionId = [string]$record.payload.id
        continue
    }

    if ($record.type -eq "event_msg" -and $record.payload.type -eq "task_started") {
        $currentTurnEntryIndexes.Clear()
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
        foreach ($index in $currentTurnEntryIndexes) {
            $entries[$index].RolledBack = $true
        }
        $rollbackEvents.Add([pscustomobject]@{
            Line      = $lineNumber
            Timestamp = $timestampText
            NumTurns  = [int]$record.payload.num_turns
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
[void]$transcript.AppendLine("# Origin conversation - verbatim")
[void]$transcript.AppendLine()
[void]$transcript.AppendLine("This is the complete canonical human/assistant conversation captured from the original Codex session through the recorded cutoff. Message bodies are unchanged. Headings and timestamps are the only additions.")
[void]$transcript.AppendLine()
[void]$transcript.AppendLine("- Session: ``$sessionId``")
[void]$transcript.AppendLine("- Cutoff: ``$CutoffTimestamp``")
[void]$transcript.AppendLine("- Canonical entries: $($canonicalEntries.Count)")
[void]$transcript.AppendLine("- Extraction details: [provenance.md](provenance.md)")
[void]$transcript.AppendLine()

$sequence = 0
foreach ($entry in $canonicalEntries) {
    $sequence++
    $anchor = "T{0:D3}" -f $sequence
    $kindSuffix = if ($entry.Kind -eq "message") { "" } else { " - $($entry.Kind)" }
    [void]$transcript.AppendLine("## $anchor - $($entry.Role)$kindSuffix")
    [void]$transcript.AppendLine()
    [void]$transcript.AppendLine("``$($entry.Timestamp)``")
    [void]$transcript.AppendLine()

    if ($entry.Kind -eq "message") {
        [void]$transcript.Append($entry.Text)
        if (-not $entry.Text.EndsWith("`n")) {
            [void]$transcript.AppendLine()
        }
    }
    else {
        [void]$transcript.AppendLine('~~~json')
        [void]$transcript.AppendLine($entry.Text)
        [void]$transcript.AppendLine('~~~')
    }
    [void]$transcript.AppendLine()
}

$utf8NoBom = [Text.UTF8Encoding]::new($false)
[IO.File]::WriteAllText($resolvedOutputPath, $transcript.ToString(), $utf8NoBom)

$provenance = [Text.StringBuilder]::new()
[void]$provenance.AppendLine("# Transcript provenance")
[void]$provenance.AppendLine()
[void]$provenance.AppendLine("## Source")
[void]$provenance.AppendLine()
[void]$provenance.AppendLine("- Session ID: ``$sessionId``")
[void]$provenance.AppendLine("- Source file: ``$([IO.Path]::GetFileName($resolvedSessionPath))``")
[void]$provenance.AppendLine("- Cutoff timestamp: ``$CutoffTimestamp``")
[void]$provenance.AppendLine("- Raw user/assistant message records through cutoff: $($messageEntries.Count)")
[void]$provenance.AppendLine("- Rolled-back message records excluded from the canonical conversation: $($rolledBackEntries.Count)")
[void]$provenance.AppendLine("- Interactive prompt/response records included: $($interactiveEntries.Count)")
[void]$provenance.AppendLine("- Canonical transcript entries: $($canonicalEntries.Count)")
[void]$provenance.AppendLine()
[void]$provenance.AppendLine("## Inclusion rules")
[void]$provenance.AppendLine()
[void]$provenance.AppendLine("- Include every ``response_item`` message whose role is ``user`` or ``assistant``.")
[void]$provenance.AppendLine("- Include ``request_user_input`` prompts and their matching user responses because they contain visible conversation decisions.")
[void]$provenance.AppendLine("- Preserve message text exactly as stored. Add only transcript headings and timestamps.")
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

[IO.File]::WriteAllText($resolvedProvenancePath, $provenance.ToString(), $utf8NoBom)

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
