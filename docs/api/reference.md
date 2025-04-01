# Reference

---

## Base URL

https://pet-toxins-api.up.railway.app/
>```bash
>BASE_URL = https://pet-toxins-api.up.railway.app/
>```

---

## Response Object Fields

| Field           | Type     | Description                                  |
|-----------------|----------|----------------------------------------------|
| `toxin_id`      | Integer  | Unique database ID                           |
| `name`          | String   | Common name of the toxin                     |
| `category`      | String   | Toxin category (e.g. Foods, Plants)          |
| `description`   | String   | Toxicology summary                           |
| `symptoms`      | String   | Symptoms as comma-separated text             |
| `alternate_names` | String | Alternative or slang names                   |
| `image_url`     | String   | Link to toxin image                          |
| `link`          | String   | URL to full source page                      |
| `animals`       | Object   | Key-value pair of species to severity string |

**Note:**

- The `animals` field will return an empty object (`{}`) if no data is available.
- All other fields will return `null` if that information is missing.

---

## Example Response

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

---

## Categories

### category

> `Envenomations`, `Fertilizers`, `Foods`, `Garage Items`, `Garden Items`, `Herbals`, `Household Items`, `Illicit Drugs`, `Insecticides`, `Medications`, `Metals`, `Plants`, `Topical Medications`, `Toxic Gases`

### animals

> `Birds`, `Cats`, `Cows`, `Dogs`, `Horses`
