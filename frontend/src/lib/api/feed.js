import { api } from "./client";

// Shared community feed. Works signed out while the backend's feed is public;
// when signed in, the token is sent so posts include the viewer's own reaction.
export const feedApi = {
  getFeed: (query) => api.get("/feed/", { query }),
};
