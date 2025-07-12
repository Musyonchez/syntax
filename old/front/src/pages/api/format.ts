import { spawn } from 'child_process'
import { NextApiRequest, NextApiResponse } from 'next';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
    const { code, language } = req.body;

    if (language === "python") {
        const process = spawn("python3", ["src/ast/python/format.py"]);

        process.stdin.write(code);
        process.stdin.end();

        let output = "";
        process.stdout.on("data", (data) => {
          output += data.toString();
        });
    
        process.stderr.on("data", (data) => {
          console.error(`stderr: ${data}`);
        });


    process.on("close", () => {
        if (output && typeof output === 'string') {
          try {
            const parsedOutput = JSON.parse(output);
            res.status(200).json({ code: parsedOutput });
            res.status(500).end();
            console.log("parsedOutput",parsedOutput)
          } catch (error) {
            console.error('Failed to parse JSON:', error);
            res.status(500).json({ error: 'Failed to parse JSON from the child process.' });
            res.status(500).end();
          }
        } else {
          console.error('No output or invalid JSON format received.');
          res.status(500).json({ error: 'No output or invalid JSON format received from the child process.' });
          res.status(500).end();
        }
      });
    } else {
      res.status(400).json({ error: "Unsupported language" });
      res.status(500).end();
    }
  
    // Ensure a response is sent even if the above conditions are not met
    // res.status(500).end(); // Use .end() to explicitly signal the end of the response
  }