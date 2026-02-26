UNSUPPORTED_TYPE = "UNSUPPORTED_TYPE"
EXCLUDED_BY_PATTERN = "EXCLUDED_BY_PATTERN"
FILE_TOO_LARGE = "FILE_TOO_LARGE"
READ_ERROR = "READ_ERROR"
EMPTY_FILE = "EMPTY_FILE"
LIMIT_DEPTH_EXCEEDED = "LIMIT_DEPTH_EXCEEDED"
LIMIT_MAX_FILES_REACHED = "LIMIT_MAX_FILES_REACHED"
DOCS_UNSUPPORTED_EXTENSION = "UNSUPPORTED_EXTENSION"
DOCS_FILE_NOT_FOUND = "FILE_NOT_FOUND"
DOCS_FILE_READ_ERROR = "FILE_READ_ERROR"
DOCS_EMPTY_CONTENT = "EMPTY_CONTENT"
DOCS_UNCHANGED = "UNCHANGED_DOCUMENT"
DOCS_UPSERT_FAILED = "UPSERT_FAILED"

KNOWN_SKIP_REASONS = {
    UNSUPPORTED_TYPE: "File type is not allowed by INDEX_FILE_TYPES",
    EXCLUDED_BY_PATTERN: "Path matched INDEX_EXCLUDE_PATTERNS",
    FILE_TOO_LARGE: "File exceeds INDEX_MAX_FILE_SIZE_BYTES",
    READ_ERROR: "Failed to read file content",
    EMPTY_FILE: "File has zero size",
    LIMIT_DEPTH_EXCEEDED: "File depth exceeds maxTraversalDepth",
    LIMIT_MAX_FILES_REACHED: "File skipped because maxFilesPerRun limit was reached",
    DOCS_UNSUPPORTED_EXTENSION: "File extension is not allowed by docs indexing policy",
    DOCS_FILE_NOT_FOUND: "File was not found during docs indexing",
    DOCS_FILE_READ_ERROR: "Failed to read markdown content for docs indexing",
    DOCS_EMPTY_CONTENT: "Markdown file is empty",
    DOCS_UNCHANGED: "Document hash did not change since previous docs run",
    DOCS_UPSERT_FAILED: "Failed to embed or upsert one or more chunks for document",
}

