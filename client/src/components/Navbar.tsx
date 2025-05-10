import React from "react";
import Link from "next/link";
import Image from "next/image";
import Logo from "../../public/images/logo.png";
import { useRouter } from "next/router";

const Navbar = () => {
  const router = useRouter();

  const navItems = [
    { name: "Add Snippet", path: "/add_snippet" },
    { name: "Practice", path: "/practice" },
    { name: "Leaderboard", path: "/leaderboard" },
    { name: "Login", path: "/login" },
  ];

  return (
    <header className="bg-[#000d2a] sticky top-0 z-50 shadow-md">
      <div className="max-w-7xl mx-auto flex items-center justify-between px-4 py-3">
        {/* Logo */}
        <Link href="/">
          <Image
            src={Logo}
            alt="SyntaxMem Logo"
            width={130}
            height={130}
            className="cursor-pointer"
            priority
          />
        </Link>

        {/* Navigation */}
        <nav>
          <ul className="flex space-x-6 items-center text-gray-200">
            {navItems.map(({ name, path }) => (
              <li key={name}>
                <Link
                  href={path}
                  className={`relative transition-colors duration-200 ${
                    router.pathname === path ? "text-[#A0FF70]" : "hover:text-white"
                  }`}
                >
                  {name}
                  <span
                    className={`absolute left-0 -bottom-1 h-[2px] w-full bg-[#A0FF70] transform scale-x-0 transition-transform duration-300 ease-in-out ${
                      router.pathname === path ? "scale-x-100" : "hover:scale-x-100"
                    }`}
                  />
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Navbar;
