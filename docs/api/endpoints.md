# Endpoints

---

## GET `/endpoints`

Returns all available routes and categories.

**Example:** 
>https://pet-toxins-api.up.railway.app/endpoints

**Returns**:

>```json
>{
>    "routes": [
>        { ... }, // list of route metadata objects
>    ],
>    "categories": [
>        "Envenomations",
>        ...,
>        "Toxic Gases"
>    ],
>    "animals": [
>        "Birds",
>        ...,
>        "Horses"
>    ]
>}
>```

---

## GET `/toxins`

Returns all toxin entries.  
Supports optional filters via query parameters:

**Query Parameters:**

- `name` — partial or full toxin name (case-insensitive)
- `animal` — species name (e.g., `Cats`, `Dogs`)
- `category` — type of item (e.g., `Plants`, `Foods`)

---

**Example:** 
>https://pet-toxins-api.up.railway.app/toxins?animal=Cats&category=Plants

**Returns**:
>```json
>[
>    {
>        "toxin_id": 10,
>        "name": "Andromeda Japonica",
>        "category": "plants",
>        ...,
>    },
>    {
>        "toxin_id": 11,
>        "name": "American Bittersweet",
>        "category": "plants",
>        ...,
>    ...,
>]
>```

---

## `GET /toxins/<id>`

Returns a single toxin by its ID.

**Example:** 
>https://pet-toxins-api.up.railway.app/toxins/49

**Returns**:
>```json
>{
>    "toxin_id": 49,
>    "name": "Beech Trees",
>    "category": "Plants",
>    "link": "https://www.petpoisonhelpline.com/poison/beech-trees/",
>    "image_url": "https://petpoisonhelp.wpenginepowered.com/wp-content/uploads/2011/10/Beech-Tree-452x390.jpg",
>    "alternate_names": "Beechnut, Fagus grandiflora, Fagus sylvatica",
>    "description": "This plant contains saponins and polyphenolic compounds. Fagus grandiflora, a species native to North America, is...",
>    "animals": {
>        "Dogs": {
>            "severity": "Mild"
>        },
>        "Cats": {
>            "severity": "Mild"
>       }
>    }
>}
>```
