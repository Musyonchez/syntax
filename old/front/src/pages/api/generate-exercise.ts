import { spawn } from 'child_process';
import { NextApiRequest, NextApiResponse } from 'next';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
    const { ast } = req.body;

    // Step 1: Create the exercise by modifying the AST
    const createExercise = spawn("python3", ["src/ast/python/createExercise.py"]);

    let modifiedAst = '';
    createExercise.stdin.write(JSON.stringify(ast));
    createExercise.stdin.end();

    createExercise.stdout.on('data', (data) => {
        modifiedAst += data.toString();
    });

    createExercise.on('close', (code) => {
        if (code !== 0) {
            res.status(500).json({ error: 'Error in creating exercise' });
            return;
        }

        // Step 2: Convert the modified AST back to code
        const astToCode = spawn("python3", ["src/ast/python/astToCode.py"]);
        let modifiedCode = '';

        astToCode.stdin.write(modifiedAst);
        astToCode.stdin.end();

        astToCode.stdout.on('data', (data) => {
            modifiedCode += data.toString();
        });

        astToCode.on('close', (code) => {
            if (code !== 0) {
                res.status(500).json({ error: 'Error in converting AST to code' });
                return;
            }

            // Step 3: Send the result back to the client
            res.status(200).json({ exercise: modifiedCode });
        });
    });
}
