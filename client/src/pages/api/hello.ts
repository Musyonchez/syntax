// // Next.js API route support: https://nextjs.org/docs/api-routes/introduction
// import type { NextApiRequest, NextApiResponse } from "next";

// type Data = {
//   name?: string;
//   error?: string;
// };

// export default async function handler(
//   req: NextApiRequest,
//   res: NextApiResponse<Data>
// ) {
//   // Now, a request to /api/post/abc will respond with the text: Post: abc.
//   const { pid } = req.query
//   res.end(`Post: ${pid}`)

//   const { slug } = req.query
//   res.end(`Post: ${slug.join(', ')}`)

//   res.status(200).json({ name: "John Doe" });
//   res.status(500).send({ error: 'failed to fetch data' })

//   if (req.method === "POST") {
//     // Process a POST request
//   } else {
//     // Handle any other HTTP method
//   }

//   const { name, message } = req.body
//   try {
//     await handleFormInputAsync({ name, message })
//     res.redirect(307, '/')
//   } catch (err) {
//     res.status(500).send({ error: 'Failed to fetch data' })
//   }

// }

// export const config = {
//   api: {
//     bodyParser: {
//       sizeLimit: '1mb',
//     },
//   },
//   // Specifies the maximum allowed duration for this function to execute (in seconds)
//   maxDuration: 5,
// }

// export const config = {
//   api: {
//     bodyParser: false,
//   },
// }

// export const config = {
//   api: {
//     bodyParser: {
//       sizeLimit: '500kb',
//     },
//   },
// }

// export const config = {
//   api: {
//     externalResolver: true,
//   },
// }

// export const config = {
//   api: {
//     responseLimit: false,
//   },
// }

// export const config = {
//   api: {
//     responseLimit: '8mb',
//   },
// }