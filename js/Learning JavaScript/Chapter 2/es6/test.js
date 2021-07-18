'use strict';

// es6 feature: block-scoped "let" declaration
const sentences = [
  {subject: 'JavaScript', verb: 'is', object: 'great'},
  {subject: 'Elephants', verb: 'are', object: 'large'},
];

// es6 feature: object destructuring
/**
 * Outputs a sentence to the console.
 */
function say({subject, verb, object}) {
  // es6 feature: template strings
  console.log(`${subject} ${verb} ${object}`);
}

// es6 feature: for..of
for (const s of sentences) {
  say(s);
}
