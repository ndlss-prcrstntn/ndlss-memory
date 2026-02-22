# Data Model: MCP Ingestion Reliability

## Entity: IngestionRunOutcome

**Description**: Aggregated outcome of ingestion started via MCP/REST.

### Fields

- `runId` (string, required): unique ingestion run identifier.
- `status` (enum, required): `queued | running | completed | failed | partial`.
- `totalFiles` (integer, required, >= 0): total discovered files.
- `totalChunks` (integer, required, >= 0): total produced chunks.
- `embeddedChunks` (integer, required, >= 0): successfully embedded/upserted chunks.
- `failedChunks` (integer, required, >= 0): failed chunks.
- `retryCount` (integer, required, >= 0): total retry attempts.
- `errorCode` (string, optional): machine-readable failure code.
- `errorMessage` (string, optional): human-readable failure details.
- `lastEventAt` (datetime, required): latest progress timestamp.

### Validation Rules

- `embeddedChunks + failedChunks <= totalChunks`
- `status=completed` implies `errorCode` is empty.
- `status=failed` implies `errorCode` is present.

### State Transitions

- `queued -> running -> completed`
- `queued -> running -> failed`
- `running -> partial` (if completion with recoverable failures is supported)

## Entity: VectorCollectionState

**Description**: Runtime observability state for target Qdrant collection used by ingestion/search.

### Fields

- `collectionName` (string, required): expected collection identifier.
- `exists` (boolean, required): collection existence flag.
- `pointsCount` (integer, required, >= 0): point count at check time.
- `checkedAt` (datetime, required): verification timestamp.

### Validation Rules

- For non-empty indexed test dataset, successful run should produce `exists=true` and `pointsCount > 0`.
- `exists=false` implies `pointsCount=0`.

## Entity: RuntimePortConfig

**Description**: Effective networking config across compose stack.

### Fields

- `qdrantExternalPort` (integer, required, > 0): host-exposed Qdrant port (`QDRANT_PORT`).
- `qdrantInternalPort` (integer, required, > 0): service-to-service Qdrant port (`QDRANT_API_PORT`).
- `mcpPort` (integer, required, > 0): host-exposed MCP port.
- `workspacePath` (string, required): mounted workspace path.

### Validation Rules

- `qdrantInternalPort` defaults to `6333` unless explicitly overridden.
- Changing `qdrantExternalPort` must not break service-to-service connectivity.

## Entity: SmokeRegressionResult

**Description**: Output of automated regression scenario.

### Fields

- `runId` (string, required): regression run identifier.
- `scenario` (enum, required): `collection_creation | custom_external_port`.
- `status` (enum, required): `passed | failed`.
- `artifacts` (array[string], required): produced artifact paths.
- `failureCode` (string, optional): machine-readable failure reason.
- `failureMessage` (string, optional): descriptive failure text.
- `finishedAt` (datetime, required): completion timestamp.

### Relationships

- `SmokeRegressionResult` references one `IngestionRunOutcome`.
- `SmokeRegressionResult` includes observed `VectorCollectionState`.
- `SmokeRegressionResult` is evaluated against one `RuntimePortConfig`.
