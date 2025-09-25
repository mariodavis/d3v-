A simple, self-contained JavaScript snippet that detects popular frontend **frameworks** and **libraries** used by any website.  
It also shows **version numbers** when available (e.g., React, Vue, AngularJS, jQuery).  

- Detects frameworks & libraries such as:
  - React.js (with version)
  - Next.js
  - Gatsby.js
  - AngularJS (with version)
  - Angular (modern)
  - Vue.js (with version)
  - Svelte.js / SvelteKit
  - jQuery.js (with version)
  - Backbone.js
  - Ember.js
  - Meteor.js
  - Zepto.js
  - can.js
  - fq.js
- Outputs a clean JSON-like object with detected technologies.
- Lightweight and dependency-free.
- Runs directly in the browser console.
## Usage
1. Open the website you want to analyze.
2. Open **Developer Tools → Console**:
   - Windows/Linux: `Ctrl + Shift + I`
   - Mac: `Cmd + Option + I`
3. Paste the script from `detector.js` into the console and press **Enter**.
4. The console will print detected frameworks/libraries and their versions (if available).

## 📝 Example Output
```js
✅ Detected frameworks/libraries: {
  "React.js": "18.2.0",
  "jQuery.js": "3.7.1"
}

