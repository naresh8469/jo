# Sharma Kirana Store — App Prototype

Ye ek working React prototype hai jisme customer app (home, search, cart,
checkout, order tracking, wishlist) aur shop admin panel (products, stock,
orders, reports) dono shamil hain. Abhi ye demo data ke saath chalta hai —
real database/backend nahi juda hai, isliye refresh karne par cart/orders
reset ho jayenge.

## StackBlitz par turant test karne ke liye (phone/PC dono se)

1. https://stackblitz.com kholo, "Create new project" → "React (Vite)" chuno.
2. Is zip ke andar `src/App.jsx` ka poora content copy karke StackBlitz ke
   `src/App.jsx` me paste kar do (StackBlitz ka apna App.jsx replace kar do).
3. `src/main.jsx` bhi isi tarah replace kar do.
4. Left panel me Dependencies me `lucide-react` add karo.
5. Save hote hi live preview URL mil jayega — usse kisi ko bhi share kar
   sakte ho.

## Apne computer par chalane ke liye (agar Node.js installed hai)

```
npm install
npm run dev
```

Browser me `http://localhost:5173` khul jayega.

## Free hosting par live karne ke liye (Vercel / Netlify)

1. Is folder ko GitHub repo me upload karo (GitHub app se mobile se bhi
   ho sakta hai, ya https://github.com/new se naya repo bana ke files
   upload karo).
2. https://vercel.com ya https://netlify.com par jaake "Import from
   GitHub" karo, apna repo chuno.
3. Framework "Vite" auto-detect ho jayega — bas "Deploy" dabao.
4. 1-2 minute me ek free `.vercel.app` ya `.netlify.app` link mil jayega
   jo hamesha live rahega (jab tak aap chaho).

Isi project ko baad me real backend (Firebase ya Render + database) se
jodkar asli offline-sync kirana app banaya ja sakta hai — jaisa humne
pehle discuss kiya tha.
