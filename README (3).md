# AI Agent Backend (Central Brain)

Ye backend aapke PC app aur phone app dono ke liye "brain" ka kaam karega.
Dono devices isi server se baat karenge, isliye context/memory sync rahega.

## Endpoints

| Endpoint         | Method | Kaam                                                        |
|-------------------|--------|--------------------------------------------------------------|
| `/`               | GET    | Health check (server chal raha hai ya nahi)                 |
| `/chat`           | POST   | Normal AI conversation (assistant ki tarah baat karna)      |
| `/task`           | POST   | Automation command ko structured action me convert karna    |
| `/memory`         | GET    | Poori saved history/facts dekhna                             |
| `/memory/fact`    | POST   | Ek permanent fact/preference save karna                     |

Har request me header chahiye: `X-API-Key: <aapka API_SECRET>`

### `/chat` example

```
POST /chat
{
  "message": "Aaj ka schedule bata do",
  "device": "phone"
}
```

### `/task` example

```
POST /task
{
  "command": "Chrome khol do",
  "device": "pc"
}
```

Response:
```
{ "action": { "action": "open_app", "target": "chrome", "params": {} } }
```

PC/phone app is JSON response ko padh kar actual action perform karega
(server khud koi app open nahi karta — sirf batata hai kya karna hai).

## Render pe Deploy Karne Ke Steps

1. Ye poora folder GitHub repo me push karo (naya repo banao, e.g. `ai-agent-backend`).
2. Render dashboard me jao -> **New +** -> **Web Service**.
3. Apna GitHub repo connect karo.
4. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn main:app`
   - **Plan:** Free
5. Environment Variables add karo (Render dashboard -> Environment):
   - `GROQ_API_KEY` = apni Groq API key (console.groq.com se lo, free hai)
   - `API_SECRET` = koi bhi strong password (ye aapke PC/phone app me bhi use hoga)
   - `GROQ_MODEL` = `llama-3.3-70b-versatile` (default, chahe to badal sakte ho)
6. Deploy karo. Kuch minute me URL milega jaise:
   `https://ai-agent-backend-xxxx.onrender.com`

## Test Karna

Deploy hone ke baad, apne PC se test karo (curl ya Postman se):

```bash
curl -X POST https://your-app.onrender.com/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_secret" \
  -d '{"message": "Hello, kaise ho?", "device": "pc"}'
```

Agar reply mile, matlab backend ready hai — ab PC app aur phone app isse
connect kar sakte ho.

## Next Steps

1. **Backend ready** (ye) — done
2. **PC app** — desktop client jo `/chat` aur `/task` ko call kare, aur
   actions (app open, script run) locally execute kare
3. **Phone app** — Android app jo voice command sune, backend ko bheje,
   aur response ke hisaab se phone control kare
4. **Database upgrade** — abhi memory ek simple JSON file me store ho rahi
   hai; production ke liye Supabase/Firebase free tier use karna better hoga
   taaki Render restart hone pe data na khoye

## Note

Render ka free tier service kuch der inactive rehne pe "sleep" ho jata hai
aur agli request pe ~30-50 second lagti hai wake up hone me. Agar ye
acceptable nahi hai to paid tier ya UptimeRobot jaisi free ping service
use kar sakte ho.
