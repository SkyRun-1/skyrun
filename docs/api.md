# SkyRun API Documentation

## Overview

SkyRun API provides a complete set of RESTful endpoints for content generation, review, and blockchain operations. All endpoints follow the OpenAPI specification and support asynchronous operations and real-time status queries.

## Authentication

All API requests require a JWT token in the Header:

```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Content Generation

#### POST /api/v1/content/generate

Generate new creative content.

**Request Body:**
```json
{
    "prompt": "string",
    "style": "string",
    "duration": "integer",
    "resolution": "string",
    "parameters": {
        "temperature": "float",
        "top_p": "float",
        "guidance_scale": "float"
    }
}
```

**Response:**
```json
{
    "content_id": "string",
    "status": "string",
    "estimated_time": "integer",
    "task_id": "string"
}
```

### Content Review

#### POST /api/v1/content/review

Submit content for review.

**Request Body:**
```json
{
    "content_id": "string",
    "review_type": "string",
    "priority": "integer",
    "metadata": {
        "category": "string",
        "tags": ["string"]
    }
}
```

**Response:**
```json
{
    "review_id": "string",
    "status": "string",
    "score": "float",
    "feedback": "string",
    "timestamp": "string"
}
```

### Content Registration

#### POST /api/v1/blockchain/register

Register content ownership on the blockchain.

**Request Body:**
```json
{
    "content_id": "string",
    "owner_address": "string",
    "metadata": {
        "title": "string",
        "description": "string",
        "license": "string"
    }
}
```

**Response:**
```json
{
    "transaction_hash": "string",
    "status": "string",
    "block_number": "integer",
    "timestamp": "string"
}
```

### Content Transfer

#### POST /api/v1/blockchain/transfer

Transfer content ownership.

**Request Body:**
```json
{
    "content_id": "string",
    "from_address": "string",
    "to_address": "string",
    "price": "string",
    "metadata": {
        "reason": "string",
        "terms": "string"
    }
}
```

**Response:**
```json
{
    "transaction_hash": "string",
    "status": "string",
    "block_number": "integer",
    "timestamp": "string"
}
```

## Status Codes

- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 429: Too Many Requests
- 500: Internal Server Error

## Error Response

All error responses follow this format:

```json
{
    "error": {
        "code": "string",
        "message": "string",
        "details": {}
    }
}
```

## Rate Limits

- Free tier: 10 requests/minute
- Pro tier: 100 requests/minute
- Enterprise tier: 1000 requests/minute

## WebSocket Interface

### Real-time Status Updates

#### WS /ws/v1/status

For receiving real-time task status updates.

**Message Format:**
```json
{
    "type": "status_update",
    "task_id": "string",
    "status": "string",
    "progress": "float",
    "timestamp": "string"
}
```

## SDK Examples

### Python

```python
from skyrun import SkyRunClient

client = SkyRunClient(api_key="your_api_key")

# Generate content
response = client.generate_content(
    prompt="A beautiful sunset over mountains",
    style="realistic",
    duration=10
)

# Get status
status = client.get_task_status(response.task_id)
```

### JavaScript

```javascript
const { SkyRunClient } = require('skyrun');

const client = new SkyRunClient({
    apiKey: 'your_api_key'
});

// Generate content
const response = await client.generateContent({
    prompt: 'A beautiful sunset over mountains',
    style: 'realistic',
    duration: 10
});

// Get status
const status = await client.getTaskStatus(response.taskId);
``` 