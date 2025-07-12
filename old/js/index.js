const acorn = require('acorn');
const escodegen = require('escodegen');

function generateOppositeQuiz(code, maxLines = 10) {
    const ast = acorn.parse(code, { ecmaVersion: 2020 });

    let sections = splitIntoSections(code, maxLines);

    // Generate quizzes for each section
    let quizzes = sections.map((section) => {
        const sectionAst = acorn.parse(section, { ecmaVersion: 2020 });

        walkAst(sectionAst, (node) => {
            if (node.type === 'FunctionDeclaration') {
                node.type = 'Placeholder'; // Remove the keyword 'function'
            } else if (node.type === 'BlockStatement') {
                node.body = []; // Remove braces
            } else if (node.type === 'BinaryExpression') {
                node.operator = '_____'; // Replace operators
            } else if (node.type === 'CallExpression') {
                node.callee.name = '_____'; // Replace structural syntax
            }
        });

        return escodegen.generate(sectionAst);
    });

    return { original: code, quizzes };
}

// Split code into sections based on a max line count
function splitIntoSections(code, maxLines) {
    const lines = code.split('\n');
    let sections = [];
    for (let i = 0; i < lines.length; i += maxLines) {
        sections.push(lines.slice(i, i + maxLines).join('\n'));
    }
    return sections;
}

function walkAst(node, callback) {
    callback(node);
    for (let key in node) {
        if (node[key] && typeof node[key] === 'object') {
            walkAst(node[key], callback);
        }
    }
}

module.exports = { generateOppositeQuiz };

// Quiz content
const quizContent = `
function greet(name) {
    const message = "Hello, " + name;
    console.log(message);
}
`;

// Generate quizzes
const quizzes = generateOppositeQuiz(quizContent);

// Print results
console.log("Original code:");
console.log(quizzes.original);
console.log("\nGenerated quizzes:");
quizzes.quizzes.forEach((quiz, index) => {
    console.log(`Quiz ${index + 1}:`);
    console.log(quiz);
});
