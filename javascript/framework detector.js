/**
 * Web Framework & Library Detector
 * --------------------------------
 * Paste into a website's browser console to detect common frontend frameworks.
 * Reports framework/library names along with versions (if available).
 */

(function () {
  /**
   * Utility function to safely query the DOM
   */
  const $ = (selector) => document.querySelector(selector);

  /**
   * Framework detection rules
   * Each entry is: name, detection condition, optional version extractor
   */
  const rules = [
    {
      name: "React.js",
      detect: () =>
        !!window.React ||
        !!$("[data-reactroot], [data-reactid]") ||
        Array.from(document.querySelectorAll("*")).some(
          (el) =>
            el._reactRootContainer !== undefined ||
            Object.keys(el).some((k) => k.startsWith("__reactContainer"))
        ),
      version: () => window.React?.version,
    },
    {
      name: "Next.js",
      detect: () => !!$("script[id=__NEXT_DATA__]"),
    },
    {
      name: "Gatsby.js",
      detect: () => !!$("#___gatsby"),
    },
    {
      name: "AngularJS",
      detect: () =>
        !!window.angular ||
        !!document.querySelector(
          ".ng-binding, [ng-app], [data-ng-app], [ng-controller], [data-ng-controller], [ng-repeat], [data-ng-repeat]"
        ) ||
        !!document.querySelector(
          'script[src*="angular.js"], script[src*="angular.min.js"]'
        ),
      version: () => window.angular?.version?.full,
    },
    {
      name: "Angular",
      detect: () =>
        !!window.getAllAngularRootElements || !!window.ng?.coreTokens?.NgZone,
    },
    {
      name: "Svelte.js / SvelteKit",
      detect: () =>
        !!$("[data-svelte-h]") ||
        !!document.querySelector("sveltekit-endpoint, sveltekit-app"),
    },
    {
      name: "Vue.js",
      detect: () => !!window.Vue,
      version: () => window.Vue?.version,
    },
    {
      name: "jQuery.js",
      detect: () => !!window.jQuery,
      version: () => window.jQuery?.fn?.jquery,
    },
    {
      name: "Backbone.js",
      detect: () => !!window.Backbone,
    },
    {
      name: "Ember.js",
      detect: () => !!window.Ember,
    },
    {
      name: "Meteor.js",
      detect: () => !!window.Meteor,
    },
    {
      name: "Zepto.js",
      detect: () => !!window.Zepto,
    },
    {
      name: "can.js",
      detect: () => !!window.can,
    },
    {
      name: "fq.js",
      detect: () =>
        !!document.querySelector("script[src*='fq.js']") || !!$("#fq-root"),
    },
  ];

 
  const detected = {};
  rules.forEach(({ name, detect, version }) => {
    try {
      if (detect()) {
        detected[name] = version ? version() || "present (version hidden)" : "present";
      }
    } catch (err) {
      console.warn(`Detection error for ${name}:`, err);
    }
  });

  /**
   * Output results
   */
  if (Object.keys(detected).length > 0) {
    console.log("✅ Detected frameworks/libraries:", detected);
  } else {
    console.log("❌ No known frameworks detected.");
  }

  return detected;
})();
