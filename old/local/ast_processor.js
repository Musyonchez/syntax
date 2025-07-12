const babel = require('@babel/core');
const traverse = require('@babel/traverse').default;
const generate = require('@babel/generator').default;
const types = require('@babel/types');

function createBlanks(code) {
    const ast = babel.parse(code, {
        sourceType: "module",
        plugins: ["jsx"]
    });

    const elementsToRemove = [];
    const placeholders = {};

    traverse(ast, {
        enter(path) {
            if (types.isVariableDeclaration(path.node)) {
                elementsToRemove.push({ type: 'VariableDeclaration', node: path.node });
            } else if (types.isFunctionDeclaration(path.node)) {
                elementsToRemove.push({ type: 'FunctionDeclaration', node: path.node });
            } else if (types.isAwaitExpression(path.node)) {
                elementsToRemove.push({ type: 'AwaitExpression', node: path.node });
            } else if (types.isReturnStatement(path.node)) {
                elementsToRemove.push({ type: 'ReturnStatement', node: path.node });
            } else if (types.isCallExpression(path.node)) {
                elementsToRemove.push({ type: 'CallExpression', node: path.node });
            }
        }
    });

    elementsToRemove.forEach((element, index) => {
        const placeholder = `__PLACEHOLDER_${index}__`;
        placeholders[placeholder] = generate(element.node).code;
        element.node.start = placeholder;
        element.node.end = "";
    });

    const blankedCode = generate(ast).code;

    return { blankedCode, placeholders };
}

const code = process.argv[2];
const result = createBlanks(code);
console.log(JSON.stringify(result));
