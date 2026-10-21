"use client";

import { useState } from "react";
import { PageHeader } from "@/components/layout/DashboardShell";
import FeedView from "@/components/posts/FeedView";
import MyPostsPanel from "@/components/posts/MyPostsPanel";
import {
  useAlumniFeed,
  useAlumniPosts,
  useCreateAlumniPost,
  useDeleteAlumniPost,
  useUpdateAlumniPost,
  useUploadPostMedia,
} from "@/hooks/useAlumni";

const ALUMNI_POST_HOOKS = {
  usePosts: useAlumniPosts,
  useCreate: useCreateAlumniPost,
  useUpdate: useUpdateAlumniPost,
  useDelete: useDeleteAlumniPost,
  useUpload: useUploadPostMedia,
};

export default function AlumniPostsPage() {
  const [tab, setTab] = useState("mine");

  return (
    <>
      <PageHeader
        title="Posts & Feed"
        subtitle="Share updates with the community and see what others are posting."
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
        {tab === "mine" ? <MyPostsPanel hooks={ALUMNI_POST_HOOKS} /> : <FeedView useFeed={useAlumniFeed} />}
      </div>
    </>
  );
}
