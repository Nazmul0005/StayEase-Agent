# API Contract — StayEase AI Agent

Base URL: `http://localhost:8000`

---

## POST `/api/chat/{conversation_id}/message`

Send a guest message to the AI agent and receive a reply.

### Path Parameters

| Parameter           | Type   | Description                                         |
| ------------------- | ------ | --------------------------------------------------- |
| `conversation_id` | string | Unique session identifier (e.g. UUID or any string) |

### Request

**Headers:**

```
Content-Type: application/json
```

**Body:**

```json
{
  "message": "string (required, min length 1)"
}
```

### Response — 200 OK

```json
{
  "conversation_id": "string",
  "reply": "string",
  "should_escalate": false,
  "timestamp": "string (ISO 8601 UTC)"
}
```

### Example — Greeting

**Request:**

```http
POST /api/chat/conv-001/message
Content-Type: application/json

{
  "message": "Hello!"
}
```

**Response:**

```json
{
  "conversation_id": "conv-001",
  "reply": "Hello! Welcome to StayEase 👋\n\nI'm your AI booking assistant. Here's what I can help you with:\n🔍 **Search** — Find available properties by location, dates, and number of guests\n🏠 **Details** — Get full information about a specific property\n📅 **Book** — Create a confirmed booking for your stay\n\nTo get started, just tell me where you'd like to stay and your travel dates!",
  "should_escalate": false,
  "timestamp": "2025-05-01T08:25:00.000000"
}
```

### Example — Search for properties

**Request:**

```http
POST /api/chat/conv-dhaka-001/message
Content-Type: application/json

{
  "message": "I need a room in Cox's Bazar for 2 nights starting May 1st for 2 guests"
}
```

**Response:**

```json
{
  "conversation_id": "conv-dhaka-001",
  "reply": "Great! Here are 3 available properties in Cox's Bazar for May 1–3 (2 guests):\n\n1. **Sea Pearl Beach Resort** — BDT 4,500/night\n   Amenities: WiFi, AC, Sea View, Breakfast\n\n2. **Ocean Paradise Hotel** — BDT 3,200/night\n   Amenities: WiFi, AC, Pool\n\n3. **Coral Reef Guest House** — BDT 1,800/night\n   Amenities: WiFi, Fan\n\nWould you like more details about any of these properties?",
  "should_escalate": false,
  "timestamp": "2025-05-01T08:30:00.000000"
}
```

### Example — Escalation

**Request:**

```http
POST /api/chat/conv-dhaka-001/message
Content-Type: application/json

{
  "message": "Can you recommend a good restaurant nearby?"
}
```

**Response:**

```json
{
  "conversation_id": "conv-dhaka-001",
  "reply": "I'm sorry, I can only help with searching for properties, getting listing details, and making bookings. For anything else, I'm connecting you with a human agent who will assist you shortly. Thank you for your patience!",
  "should_escalate": true,
  "timestamp": "2025-05-01T08:35:00.000000"
}
```

### Error Responses

| Status                        | Description                     | Body                                                                    |
| ----------------------------- | ------------------------------- | ----------------------------------------------------------------------- |
| `422 Unprocessable Entity`  | Request body missing or invalid | `{"detail": [{"msg": "field required", "loc": ["body", "message"]}]}` |
| `500 Internal Server Error` | Agent or database failure       | `{"detail": "Agent processing failed: <reason>"}`                     |

---

## GET `/api/chat/{conversation_id}/history`

Retrieve the full message history for a conversation session.

### Path Parameters

| Parameter           | Type   | Description                                      |
| ------------------- | ------ | ------------------------------------------------ |
| `conversation_id` | string | Session identifier matching the one used in POST |

### Response — 200 OK

```json
{
  "conversation_id": "string",
  "messages": [
    {
      "role": "user | assistant",
      "content": "string",
      "timestamp": "string (ISO 8601 UTC)"
    }
  ],
  "total_messages": 4
}
```

### Example

**Request:**

```http
GET /api/chat/conv-dhaka-001/history
```

**Response:**

```json
{
  "conversation_id": "conv-dhaka-001",
  "messages": [
    {
      "role": "user",
      "content": "I need a room in Cox's Bazar for 2 nights starting May 1st for 2 guests",
      "timestamp": "2025-05-01T08:30:00.000000"
    },
    {
      "role": "assistant",
      "content": "Great! Here are 3 available properties in Cox's Bazar for May 1–3 (2 guests):\n\n1. **Sea Pearl Beach Resort** — BDT 4,500/night...",
      "timestamp": "2025-05-01T08:30:02.000000"
    },
    {
      "role": "user",
      "content": "Tell me more about Sea Pearl Beach Resort",
      "timestamp": "2025-05-01T08:31:00.000000"
    },
    {
      "role": "assistant",
      "content": "Here are the details for Sea Pearl Beach Resort:\n\n📍 Kolatoli Beach Road, Cox's Bazar\n💰 BDT 4,500 per night\n👥 Up to 4 guests\n\n**Amenities:** WiFi, AC, Sea View, Breakfast included\n**House Rules:** No smoking. Check-in after 2pm, check-out by 12pm.\n\nWould you like to book this property?",
      "timestamp": "2025-05-01T08:31:02.000000"
    }
  ],
  "total_messages": 4
}
```

**Empty conversation (never messaged before):**

```json
{
  "conversation_id": "conv-new-999",
  "messages": [],
  "total_messages": 0
}
```

### Error Responses

| Status                        | Description      | Body                                    |
| ----------------------------- | ---------------- | --------------------------------------- |
| `500 Internal Server Error` | Database failure | `{"detail": "Internal server error"}` |

---

## GET `/api/listings/`

Retrieve all currently available property listings.

### Response — 200 OK

```json
[
  {
    "id": "uuid",
    "name": "Sea Pearl Beach Resort",
    "location": "Cox's Bazar",
    "address": "Kolatoli Beach Road, Cox's Bazar",
    "price_per_night": 4500.0,
    "max_guests": 4,
    "amenities": ["WiFi", "AC", "Sea View"],
    "photo_urls": ["https://..."],
    "house_rules": "No smoking...",
    "is_available": true
  }
]
```

---

## GET `/api/listings/bookings/{booking_id}`

Retrieve a single booking record by its UUID.

### Path Parameters

| Parameter    | Type   | Description           |
| ------------ | ------ | --------------------- |
| `booking_id` | string | Unique booking ID (UUID) |

### Response — 200 OK

```json
{
  "id": "uuid",
  "listing_id": "uuid",
  "guest_name": "Rahim Uddin",
  "guest_phone": "01712345678",
  "check_in": "2025-05-01",
  "check_out": "2025-05-03",
  "guests": 2,
  "total_price": 9000.0,
  "status": "confirmed",
  "created_at": "2025-04-27T12:00:00.000000"
}
```

---

## Booking Flow — Full 3-turn Example

```
Turn 1: User searches → Agent returns property list
Turn 2: User asks for details → Agent returns full listing info  
Turn 3: User confirms booking → Agent creates booking and returns confirmation
```

**Turn 3 — Booking confirmation:**

Request:

```json
{
  "message": "Yes, please book Sea Pearl Beach Resort. My name is Rahim Uddin, phone 01712345678"
}
```

Response:

```json
{
  "conversation_id": "conv-dhaka-001",
  "reply": "✅ Booking confirmed! Here's your summary:\n\n🏨 Sea Pearl Beach Resort, Cox's Bazar\n📅 May 1 – May 3, 2025 (2 nights)\n👥 2 guests\n💰 Total: BDT 9,000\n🔖 Booking ID: 3f7a9c21-...\n\nThank you, Rahim! Have a wonderful stay.",
  "should_escalate": false,
  "timestamp": "2025-05-01T08:32:05.000000"
}
```
