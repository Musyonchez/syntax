// components/home/ScreenshotSection.tsx

import Image from "next/image";

const ScreenshotSection = () => (
  <section className="py-20 px-6">
    <div className="shadow-lg rounded-lg overflow-hidden border border-[#A0FF70]">
      {/* Mobile image */}
      <Image
        src="/images/practice-screenshot-mobile.png"
        alt="Practice Quiz Screenshot (Mobile)"
        width={500} // Adjust as needed
        height={300}
        className="w-full h-auto block sm:hidden"
      />

      {/* Desktop image */}
      <Image
        src="/images/practice-screenshot-laptop.png"
        alt="Practice Quiz Screenshot"
        width={1000}
        height={600}
        className="w-full h-auto hidden sm:block"
      />
    </div>
  </section>
);

export default ScreenshotSection;
