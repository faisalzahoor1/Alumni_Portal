import PostCard from "@/components/posts/PostCard";

// Students can read community posts but not edit them, so no actions are attached.
export default function StudentPostCard({ post }) {
  return <PostCard post={post} />;
}
