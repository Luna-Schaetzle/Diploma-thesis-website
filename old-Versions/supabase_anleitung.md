Natürlich! Supabase ist eine leistungsstarke Open-Source-Alternative zu Firebase und bietet eine vollständige Backend-Infrastruktur, die auf PostgreSQL basiert. Es umfasst Funktionen wie Authentifizierung, Datenbanken, Echtzeit-Abonnements, Speicher und mehr. Für dein Projekt bietet Supabase eine einfache Möglichkeit, Benutzerdaten zu speichern und zu verwalten, ohne sich um die Verwaltung eigener Server kümmern zu müssen.

Im Folgenden erkläre ich dir, wie du Supabase in deine Schüler-KI-Plattform integrieren kannst:

## Inhaltsverzeichnis

1. [Supabase Überblick](#supabase-überblick)
2. [Projekt einrichten](#projekt-einrichten)
3. [Supabase mit Vue.js integrieren](#supabase-mit-vuejs-integrieren)
4. [Authentifizierung einrichten](#authentifizierung-einrichten)
5. [Datenbank konfigurieren](#datenbank-konfigurieren)
6. [Kontomodell implementieren](#kontomodell-implementieren)
7. [Sicherheit und Best Practices](#sicherheit-und-best-practices)
8. [Deployment](#deployment)
9. [Weiterführende Ressourcen](#weiterführende-ressourcen)

## Supabase Überblick

Supabase bietet folgende Hauptkomponenten:

- **Datenbank**: Eine PostgreSQL-Datenbank mit Echtzeit-Funktionen.
- **Authentifizierung**: Benutzerregistrierung, -anmeldung und -verwaltung.
- **Storage**: Datei-Uploads und -Verwaltung.
- **Echtzeit**: Realtime-Abonnements für Datenbankänderungen.
- **Edge Functions**: Serverless-Funktionen für erweiterte Backend-Logik.

Für dein Projekt wirst du hauptsächlich die Datenbank und die Authentifizierungsdienste von Supabase nutzen.

## Projekt einrichten

### 1. Supabase Konto erstellen

1. Gehe zu [Supabase](https://supabase.com/) und erstelle ein kostenloses Konto.
2. Nach der Anmeldung erstelle ein neues Projekt:
   - **Projektname**: z.B. `schueler-ki-plattform`
   - **Passwort**: Ein sicheres Passwort für die Datenbank.
   - **Region**: Wähle die nächstgelegene Region.

### 2. Supabase-Client konfigurieren

Supabase bietet SDKs für verschiedene Frontend-Frameworks, einschließlich Vue.js. Du benötigst die `supabase-js` Bibliothek.

## Supabase mit Vue.js integrieren

### 1. Supabase SDK installieren

Navigiere in dein Vue.js-Projektverzeichnis und installiere das Supabase SDK:

```bash
npm install @supabase/supabase-js
# oder
yarn add @supabase/supabase-js
```

### 2. Supabase-Client initialisieren

Erstelle eine Datei `src/supabase.js` und initialisiere den Supabase-Client:

```javascript
// src/supabase.js
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.VUE_APP_SUPABASE_URL
const supabaseAnonKey = process.env.VUE_APP_SUPABASE_ANON_KEY

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
```

### 3. Umgebungsvariablen konfigurieren

Erstelle oder aktualisiere deine `.env` Datei im Root-Verzeichnis deines Projekts:

```env
VUE_APP_SUPABASE_URL=https://your-supabase-url.supabase.co
VUE_APP_SUPABASE_ANON_KEY=your-anon-key
```

**Hinweis**: Ersetze `your-supabase-url` und `your-anon-key` mit den tatsächlichen Werten aus deinem Supabase-Projekt. Diese findest du im Supabase-Dashboard unter **Project Settings > API**.

## Authentifizierung einrichten

Supabase bietet einfache Methoden zur Benutzerregistrierung und -anmeldung.

### 1. Registrierung und Anmeldung

#### Registrierung (`Register.vue`):

```vue
<template>
  <form @submit.prevent="register">
    <input v-model="email" type="email" placeholder="E-Mail" required />
    <input v-model="password" type="password" placeholder="Passwort" required />
    <button type="submit">Registrieren</button>
  </form>
</template>

<script>
import { supabase } from '../supabase'

export default {
  data() {
    return {
      email: '',
      password: '',
    }
  },
  methods: {
    async register() {
      const { user, error } = await supabase.auth.signUp({
        email: this.email,
        password: this.password,
      })
      if (error) {
        console.error('Registrierungsfehler:', error.message)
      } else {
        console.log('Registrierung erfolgreich:', user)
        // Optional: Weiterleitung oder Benachrichtigung
      }
    },
  },
}
</script>
```

#### Anmeldung (`Login.vue`):

```vue
<template>
  <form @submit.prevent="login">
    <input v-model="email" type="email" placeholder="E-Mail" required />
    <input v-model="password" type="password" placeholder="Passwort" required />
    <button type="submit">Anmelden</button>
  </form>
</template>

<script>
import { supabase } from '../supabase'

export default {
  data() {
    return {
      email: '',
      password: '',
    }
  },
  methods: {
    async login() {
      const { user, error } = await supabase.auth.signIn({
        email: this.email,
        password: this.password,
      })
      if (error) {
        console.error('Anmeldefehler:', error.message)
      } else {
        console.log('Anmeldung erfolgreich:', user)
        // Optional: Weiterleitung oder Benachrichtigung
      }
    },
  },
}
</script>
```

### 2. Authentifizierungsstatus überwachen

Um den Authentifizierungsstatus in deiner Anwendung zu überwachen, kannst du einen globalen Zustand (z.B. mit Vuex oder Pinia) verwenden oder den Status direkt in den Komponenten verwalten.

#### Beispiel mit Vuex:

1. **Vuex installieren** (falls noch nicht installiert):

   ```bash
   npm install vuex@next
   # oder
   yarn add vuex@next
   ```

2. **Store einrichten** (`src/store/index.js`):

   ```javascript
   import { createStore } from 'vuex'
   import { supabase } from '../supabase'

   export default createStore({
     state: {
       user: null,
     },
     mutations: {
       setUser(state, user) {
         state.user = user
       },
     },
     actions: {
       async fetchUser({ commit }) {
         const user = supabase.auth.user()
         commit('setUser', user)
       },
       async signOut({ commit }) {
         await supabase.auth.signOut()
         commit('setUser', null)
       },
     },
     getters: {
       isAuthenticated: (state) => !!state.user,
     },
   })
   ```

3. **Store in Vue.js integrieren** (`src/main.js`):

   ```javascript
   import { createApp } from 'vue'
   import App from './App.vue'
   import store from './store'

   createApp(App)
     .use(store)
     .mount('#app')
   ```

4. **Authentifizierungsstatus überwachen** (`App.vue`):

   ```vue
   <template>
     <div>
       <router-view />
     </div>
   </template>

   <script>
   import { onMounted } from 'vue'
   import { useStore } from 'vuex'

   export default {
     setup() {
       const store = useStore()

       onMounted(() => {
         store.dispatch('fetchUser')
         supabase.auth.onAuthStateChange((event, session) => {
           store.commit('setUser', session?.user || null)
         })
       })
     },
   }
   </script>
   ```

## Datenbank konfigurieren

### 1. Tabellenstruktur erstellen

Erstelle die notwendigen Tabellen in deiner Supabase-Datenbank. Gehe dazu in deinem Supabase-Dashboard zu **Database > SQL Editor** und führe das folgende SQL-Skript aus:

```sql
-- Tabelle für Benutzerprofile
CREATE TABLE profiles (
  id uuid REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
  role VARCHAR(20) DEFAULT 'schueler', -- schueler, admin, dev, student_plus
  tokens INTEGER DEFAULT 0,
  token_limit INTEGER DEFAULT 100, -- Standardlimit für Schüler
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- Trigger, um Profile bei neuer Registrierung zu erstellen
CREATE FUNCTION handle_new_user() RETURNS trigger AS $$
BEGIN
  INSERT INTO profiles(id, role, tokens, token_limit)
  VALUES (NEW.id, 'schueler', 0, 100);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER on_auth_user_created
AFTER INSERT ON auth.users
FOR EACH ROW
EXECUTE FUNCTION handle_new_user();
```

**Erklärung:**

- **profiles**: Enthält zusätzliche Informationen über die Benutzer, wie ihre Rolle und Token-Balance.
- **Trigger**: Automatisiert die Erstellung eines Profildatensatzes, sobald ein neuer Benutzer registriert wird.

### 2. Supabase-Client für Datenbankoperationen nutzen

Erstelle Funktionen, um Profile zu verwalten, z.B. Token-Verwaltung, Rollenänderung etc.

#### Beispiel: Token hinzufügen

```javascript
// src/services/profileService.js
import { supabase } from '../supabase'

export const addTokens = async (userId, tokensToAdd) => {
  const { data, error } = await supabase
    .from('profiles')
    .update({ tokens: supabase.raw('tokens + ?', [tokensToAdd]) })
    .eq('id', userId)

  if (error) throw error
  return data
}
```

#### Beispiel: Token verwenden

```javascript
export const useTokens = async (userId, tokensToUse) => {
  // Zuerst prüfen, ob der Benutzer genügend Token hat
  const { data: profile, error: fetchError } = await supabase
    .from('profiles')
    .select('tokens, token_limit')
    .eq('id', userId)
    .single()

  if (fetchError) throw fetchError
  if (profile.tokens < tokensToUse) throw new Error('Nicht genügend Token')

  // Token abziehen
  const { data, error } = await supabase
    .from('profiles')
    .update({ tokens: supabase.raw('tokens - ?', [tokensToUse]) })
    .eq('id', userId)

  if (error) throw error
  return data
}
```

### 3. Rollen und Token-Verwaltung

Implementiere Funktionen zur Verwaltung der Benutzerrollen und Token-Balance. Beispielsweise:

- **Admin-Panel**: Ermöglicht Admins, Benutzerrollen zu ändern und Token hinzuzufügen.
- **Antrag für Student+**: Schüler können Anträge stellen, die von Admins genehmigt werden müssen.

#### Beispiel: Antrag für Student+

1. **Antragsformular** (`ApplyStudentPlus.vue`):

   ```vue
   <template>
     <form @submit.prevent="apply">
       <textarea v-model="reason" placeholder="Warum benötigst du Student+?" required></textarea>
       <button type="submit">Antrag stellen</button>
     </form>
   </template>

   <script>
   import { supabase } from '../supabase'

   export default {
     data() {
       return {
         reason: '',
       }
     },
     methods: {
       async apply() {
         const user = supabase.auth.user()
         if (!user) {
           alert('Bitte melde dich zuerst an.')
           return
         }

         const { data, error } = await supabase
           .from('student_plus_applications')
           .insert([
             { user_id: user.id, reason: this.reason }
           ])

         if (error) {
           console.error('Fehler beim Stellen des Antrags:', error.message)
         } else {
           alert('Antrag erfolgreich gestellt.')
         }
       },
     },
   }
   </script>
   ```

2. **Tabelle für Anträge erstellen**:

   ```sql
   CREATE TABLE student_plus_applications (
     id SERIAL PRIMARY KEY,
     user_id uuid REFERENCES auth.users ON DELETE CASCADE,
     reason TEXT NOT NULL,
     status VARCHAR(20) DEFAULT 'pending', -- pending, approved, rejected
     created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
   );
   ```

3. **Admin-Funktion zur Genehmigung von Anträgen**:

   ```vue
   <template>
     <div>
       <h2>Student+ Anträge</h2>
       <ul>
         <li v-for="application in applications" :key="application.id">
           <p>{{ application.reason }}</p>
           <button @click="approve(application.id, application.user_id)">Genehmigen</button>
           <button @click="reject(application.id)">Ablehnen</button>
         </li>
       </ul>
     </div>
   </template>

   <script>
   import { supabase } from '../supabase'

   export default {
     data() {
       return {
         applications: [],
       }
     },
     async created() {
       const { data, error } = await supabase
         .from('student_plus_applications')
         .select('*')
         .eq('status', 'pending')

       if (error) {
         console.error('Fehler beim Laden der Anträge:', error.message)
       } else {
         this.applications = data
       }
     },
     methods: {
       async approve(id, userId) {
         // Update den Antragstatus
         const { error: updateError } = await supabase
           .from('student_plus_applications')
           .update({ status: 'approved' })
           .eq('id', id)

         if (updateError) {
           console.error('Fehler beim Genehmigen des Antrags:', updateError.message)
           return
         }

         // Update das Benutzerprofil
         const { error: profileError } = await supabase
           .from('profiles')
           .update({ role: 'student_plus', token_limit: 500 }) // Beispielwert
           .eq('id', userId)

         if (profileError) {
           console.error('Fehler beim Aktualisieren des Profils:', profileError.message)
           return
         }

         // Entferne den Antrag aus der Liste
         this.applications = this.applications.filter(app => app.id !== id)
       },
       async reject(id) {
         const { error } = await supabase
           .from('student_plus_applications')
           .update({ status: 'rejected' })
           .eq('id', id)

         if (error) {
           console.error('Fehler beim Ablehnen des Antrags:', error.message)
         } else {
           this.applications = this.applications.filter(app => app.id !== id)
         }
       },
     },
   }
   </script>
   ```

## Kontomodell implementieren

Nun, da die grundlegende Authentifizierung und Datenbankkonfiguration steht, kannst du dein Kontomodell wie folgt umsetzen:

### 1. Rollen und Token-Limits festlegen

Definiere in der `profiles` Tabelle die verschiedenen Rollen und ihre Token-Limits:

- **schueler**: Standard-Token-Limit (z.B. 100 pro Monat)
- **student_plus**: Erhöhtes Token-Limit (z.B. 500 pro Monat)
- **admin**: Unbegrenzte Token
- **dev**: Unbegrenzte Token

### 2. Monatliche Token-Zuweisung

Implementiere einen Cron-Job oder eine geplante Funktion, die monatlich die Token-Limits zurücksetzt und ungenutzte Token addiert.

#### Beispiel mit Node.js und `node-cron`:

1. **Node.js Backend einrichten** (falls noch nicht vorhanden):

   Falls du ein separates Backend benötigst, kannst du Node.js und Express verwenden. Alternativ kannst du Supabase Edge Functions nutzen.

2. **`node-cron` installieren**:

   ```bash
   npm install node-cron
   ```

3. **Cron-Job einrichten** (`cron.js`):

   ```javascript
   const { createClient } = require('@supabase/supabase-js')
   const cron = require('node-cron')
   require('dotenv').config()

   const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY)

   // Tägliche Überprüfung, ob es ein neuer Monat ist
   cron.schedule('0 0 1 * *', async () => {
     try {
       const { data: profiles, error } = await supabase.from('profiles').select('*').not('role', 'in', '(admin, dev)')

       if (error) throw error

       for (const profile of profiles) {
         let newTokens = profile.tokens + (profile.tokens < profile.token_limit ? profile.tokens : profile.token_limit)
         if (newTokens > profile.token_limit) newTokens = profile.token_limit

         await supabase
           .from('profiles')
           .update({ tokens: newTokens })
           .eq('id', profile.id)
       }

       console.log('Token-Balances erfolgreich aktualisiert.')
     } catch (err) {
       console.error('Fehler beim Aktualisieren der Token-Balances:', err.message)
     }
   })
   ```

4. **Umgebungsvariablen konfigurieren** (`.env`):

   ```env
   SUPABASE_URL=https://your-supabase-url.supabase.co
   SUPABASE_SERVICE_KEY=your-service-key
   ```

   **Hinweis**: Die `SUPABASE_SERVICE_KEY` findest du im Supabase-Dashboard unter **Project Settings > API > Service Role**. Diese Schlüssel haben volle Zugriffrechte auf die Datenbank und sollten sicher aufbewahrt werden.

5. **Cron-Job starten**:

   ```bash
   node cron.js
   ```

   **Hinweis**: Stelle sicher, dass dieser Cron-Job auf einem Server läuft, der ständig online ist. Alternativ kannst du Supabase Edge Functions oder externe Dienste wie [Heroku Scheduler](https://www.heroku.com/scheduler) verwenden.

### 3. Token-Überprüfung bei API-Aufrufen

Stelle sicher, dass bei jeder Interaktion mit den KI-Diensten überprüft wird, ob der Benutzer genügend Token hat.

#### Beispiel: Middleware für Express.js

Falls du ein Node.js Backend verwendest, kannst du eine Middleware implementieren:

```javascript
// middleware/checkTokens.js
const { supabase } = require('../supabase')

const checkTokens = async (req, res, next) => {
  const user = supabase.auth.user()
  if (!user) return res.status(401).json({ error: 'Nicht authentifiziert' })

  const { data: profile, error } = await supabase
    .from('profiles')
    .select('tokens, token_limit')
    .eq('id', user.id)
    .single()

  if (error) return res.status(500).json({ error: 'Fehler beim Laden des Profils' })
  if (profile.tokens <= 0) return res.status(403).json({ error: 'Keine Token mehr verfügbar' })

  // Optional: Token abziehen
  await supabase
    .from('profiles')
    .update({ tokens: profile.tokens - 1 })
    .eq('id', user.id)

  next()
}

module.exports = checkTokens
```

Verwende diese Middleware in deinen Routen:

```javascript
const express = require('express')
const app = express()
const checkTokens = require('./middleware/checkTokens')

app.use(express.json())

app.post('/api/use-ai', checkTokens, async (req, res) => {
  // Dein AI-Logik hier
  res.json({ message: 'AI-Dienst genutzt' })
})

app.listen(3000, () => {
  console.log('Server läuft auf Port 3000')
})
```

## Sicherheit und Best Practices

1. **Service Role Schlüssel schützen**: Der `SUPABASE_SERVICE_KEY` sollte niemals im Frontend verwendet werden. Verwende ihn nur in deinem Backend.

2. **Rollen- und Berechtigungsverwaltung**: Nutze Row-Level Security (RLS) in Supabase, um sicherzustellen, dass Benutzer nur auf ihre eigenen Daten zugreifen können.

   **Beispiel für RLS**:

   ```sql
   -- Aktivieren von RLS für die profiles Tabelle
   ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

   -- RLS-Regel hinzufügen
   CREATE POLICY "Allow users to manage their own profiles" 
   ON profiles 
   FOR ALL 
   USING (auth.uid() = id);
   ```

3. **Datenvalidierung**: Validierung der Eingaben sowohl im Frontend als auch im Backend, um Sicherheitslücken zu vermeiden.

4. **HTTPS verwenden**: Stelle sicher, dass deine Anwendung über HTTPS läuft, um die Kommunikation zu sichern.

5. **Regelmäßige Backups**: Supabase bietet automatische Backups, aber es ist eine gute Praxis, regelmäßig eigene Backups zu erstellen.

## Deployment

### 1. Frontend bereitstellen

Baue dein Vue.js-Projekt und hoste die statischen Dateien auf einem Webserver oder einer Hosting-Plattform wie Vercel, Netlify oder deinem eigenen Server.

```bash
npm run build
```

### 2. Backend bereitstellen

Falls du ein eigenes Backend verwendest (z.B. mit Node.js), hoste es auf Plattformen wie Heroku, DigitalOcean, AWS, etc.

### 3. Supabase konfigurieren

Stelle sicher, dass alle Umgebungsvariablen korrekt gesetzt sind und dass deine Anwendung auf die Supabase-Datenbank zugreifen kann.