"use client";

import { useState } from "react";
import { PageHeader } from "@/components/layout/DashboardShell";
import FeedView from "@/components/posts/FeedView";
import MyPostsPanel from "@/components/posts/MyPostsPanel";
import {
  useCreateIndustryPost,
  useDeleteIndustryPost,
  useIndustryFeed,
  useIndustryPosts,
  useUpdateIndustryPost,
  useUploadIndustryPostMedia,
} from "@/hooks/useIndustry";

const INDUSTRY_POST_HOOKS = {
  usePosts: useIndustryPosts,
  useCreate: useCreateIndustryPost,
  useUpdate: useUpdateIndustryPost,
  useDelete: useDeleteIndustryPost,
  useUpload: useUploadIndustryPostMedia,
};

export default function IndustryPostsPage() {
  const [tab, setTab] = useState("feed");

  return (
    <>
      <PageHeader
        title="Posts & Feed"
        subtitle="Share hiring news and announcements, and see what alumni are posting."
        actions={
          <div className="tabs">
            <button className={`tab ${tab === "mine" ? "tab-active" : ""}`} onClick={() => setTab("mine")}>
              My posts
            </button>
            <button className={`tab ${tab === "feed" ? "tab-active" : ""}`} onClick={() => setTab("feed")}>
              Community feed
            </button>
          </div>
        }
      />
      <div key={tab} className="fade-up">
        {tab === "mine" ? <MyPostsPanel hooks={INDUSTRY_POST_HOOKS} /> : <FeedView useFeed={useIndustryFeed} />}
      </div>
    </>
  );
}
