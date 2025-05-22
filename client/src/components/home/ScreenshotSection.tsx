// components/home/ScreenshotSection.tsx

import Image from "next/image";

const ScreenshotSection = () => (
  <section className="py-20 px-6">
    <div className="max-w-5xl mx-auto text-center">
      <h2 className="text-3xl font-bold mb-6">See It in Action</h2>
      <p className="mb-8 max-w-2xl mx-auto text-gray-300">
        Here's what the Practice page looks like once your snippet is converted.
        It's clean, focused, and ready to test your recall.
      </p>
      <div className="shadow-lg rounded-lg overflow-hidden border border-[#A0FF70]">
        <Image
          src="/images/practice-screenshot.png"
          alt="Practice Quiz Screenshot"
          width={1000}
          height={600}
          className="w-full h-auto"
        />
      </div>
    </div>
  </section>
);

export default ScreenshotSection;
