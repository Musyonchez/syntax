// components/home/DemoSnippet.tsx

const DemoSnippet = () => (
  <section className="bg-[#A0FF70] text-black py-20 px-6">
    <div className="max-w-4xl mx-auto text-center">
      <h3 className="text-2xl font-bold mb-6">
        Try It Out – No Sign Up Needed
      </h3>
      <div className="flex justify-around items-center flex-wrap gap-6">
        <div className="text-left bg-white p-6 rounded-lg shadow-md w-[300px]">
          <h4 className="text-lg font-semibold mb-2">Sample Code:</h4>
          <pre className="bg-gray-100 text-black p-4 rounded-md overflow-auto">
            {`for i in range(5):
        print(i)`}
          </pre>
        </div>

        <div className="text-left bg-white p-6 rounded-lg shadow-md w-[300px]">
          <h4 className="text-lg font-semibold mb-2">Masked Quiz Version:</h4>
          <pre className="bg-gray-100 text-black p-4 rounded-md overflow-auto">
            {`for i (____) (____)(5):
        print(____)`}
          </pre>
        </div>
      </div>
      <p className="mt-4 text-sm text-gray-700">
        Just a taste! This is how your custom snippets will look when turned
        into a quiz.
      </p>
    </div>
  </section>
);

export default DemoSnippet;
