"use client";

import React, { useEffect, useState } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import SnippetForm from "./../components/addSnippet/SnippetForm";
import SnippetTips from "./../components/addSnippet/SnippetTips";
import SnippetSuccessError from "./../components/addSnippet/SnippetSuccessError";
import { useDispatch, useSelector } from "react-redux";
import { addSnippet, setAddSnippetStatus } from "@/store/snippet_store/actions";
import { RootState } from "@/store";
import { useSession } from "next-auth/react";
import { fetchUser } from "@/store/user_store/actions";

const AddSnippetPage = () => {
  const dispatch = useDispatch();
  const { data: session } = useSession();
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [language, setLanguage] = useState("python");

  const status = useSelector((state: RootState) => state.snippet.addSnippetStatus);
  const userDBData = useSelector((state: RootState) => state.user.user);

  useEffect(() => {
    if (session?.user?.email && (!userDBData || userDBData.email !== session.user.email)) {
      dispatch(fetchUser(session.user.email));
      console.log("Dispatched fetchUser in AddSnippet");
    }
  }, [session?.user?.email, userDBData, dispatch]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || !content.trim() || !language || !userDBData) {
      return;
    }

    dispatch(addSnippet({
      title: title.trim(),
      content: content.trim(),
      language,
      createdAt: new Date().toISOString(),
      userId: String(userDBData.id),
    }));
  };

  useEffect(() => {
    if (status === "success") {
      setTitle("");
      setContent("");
      setLanguage("python");

      const timeout = setTimeout(() => {
        dispatch(setAddSnippetStatus("idle"));
      }, 3000);

      return () => clearTimeout(timeout);
    }
  }, [status, dispatch]);

  return (
    <>
      <Navbar />
      <div className="flex flex-col min-h-screen bg-[#000d2a] text-white">
        <main className="flex-grow py-10 px-6 max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold mb-4 text-center text-[#A0FF70]">
            Add a Code Snippet
          </h1>
          <p className="text-center mb-10 text-[#A0FF70]">
            Welcome to the Quiz Builder! Paste in your code, choose a language,
            and give it a name. We’ll turn it into a syntax quiz for you to master.
          </p>

          <SnippetForm
            title={title}
            setTitle={setTitle}
            content={content}
            setContent={setContent}
            language={language}
            setLanguage={setLanguage}
            handleSubmit={handleSubmit}
            isSubmitting={status === "loading"}
          />

          <SnippetSuccessError status={status} />
          <SnippetTips />
        </main>
      </div>
      <Footer />
    </>
  );
};

export default AddSnippetPage;
