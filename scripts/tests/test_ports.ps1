Set-StrictMode -Version Latest

function Set-DefaultTestPorts {
    param(
        [string]$DefaultMcpPort = "18080",
        [string]$DefaultQdrantPort = "16333"
    )

    if (-not $env:TEST_MCP_PORT) {
        $env:TEST_MCP_PORT = $DefaultMcpPort
    }
    if (-not $env:TEST_QDRANT_PORT) {
        $env:TEST_QDRANT_PORT = $DefaultQdrantPort
    }

    if (-not $env:MCP_PORT) {
        $env:MCP_PORT = $env:TEST_MCP_PORT
    }
    if (-not $env:QDRANT_PORT) {
        $env:QDRANT_PORT = $env:TEST_QDRANT_PORT
    }
}

function Get-TestMcpPort {
    if ($env:MCP_PORT) {
        return [string]$env:MCP_PORT
    }
    if ($env:TEST_MCP_PORT) {
        return [string]$env:TEST_MCP_PORT
    }
    return "18080"
}

function Get-TestQdrantPort {
    if ($env:QDRANT_PORT) {
        return [string]$env:QDRANT_PORT
    }
    if ($env:TEST_QDRANT_PORT) {
        return [string]$env:TEST_QDRANT_PORT
    }
    return "16333"
}

function Get-TestBaseUrl {
    $port = Get-TestMcpPort
    return "http://localhost:$port"
}

