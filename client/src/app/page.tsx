import { HeroSection } from "@/components/home/hero-section"
import { DemoSection } from "@/components/home/demo-section"
import { FeaturesSection } from "@/components/home/features-section"
import { CTASection } from "@/components/home/cta-section"

export default function Home() {
  return (
    <div className="flex flex-col">
      <HeroSection />
      <DemoSection />
      <FeaturesSection />
      <CTASection />
    </div>
  )
}
