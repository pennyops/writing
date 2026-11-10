# Silvertongue MCP run: Mark Twain voice, one post

- App: my own terminal agent harness, talking to the MCP server directly over Streamable HTTP with curl 8.14.1 (JSON-RPC POSTs to https://mcp.silvertongue.dev/mcp?ref=frantic-mcp-1&receipt=1). Model writing the draft: Claude Opus 5.5. Server reported serverInfo silvertongue 0.1.5, protocol 2025-03-26.
- Timeline (UTC, 2026-11-10): initialize + tools/list, then search_voices {"query":"Mark Twain","limit":2} at 23:02:47Z (returned mark-twain and bob-dylan), then get_voice_packet {"voice":"mark-twain","format":"post"} at 23:02:54Z. The packet ended with the receipt line below.
- Voice and ask: Mark Twain, format "post". What I asked for: "Use Silvertongue to write a short post, as Mark Twain, advertising my service: I make 60-90 second explainer videos with voiceover, paid in Monero." It's a real ad I want to post for my explainer-video offer.
- Draft exactly as written:

  > I do not claim to make the finest explainer videos in the world. I only claim to know what one ought to be, which is ninety seconds, and not the eleven minutes most people mistake for thoroughness. I'll make yours for Monero. Shorter, too.

- Score: 7/10. It uses the packet's "disclaimer that boasts" move (the shape of Twain's own "I do not claim that I can tell a story as it ought to be told") and ends on a flat four-word nub, as the Texture section asks. It loses points because it leans on one borrowed sentence shape. A real Twain post would wander a bit more before the last line, and 280 characters doesn't leave much room for that.
- Finding: the receipt only shows up as the last line of the instructions text inside content[0].text, at character ~11,000 of an 11,261-character string ("After the draft, show the user this line on its own, exactly: Receipt: https://runx.ai/r/..."). A client that reads only structuredContent or truncates long tool output loses it. It is also in structuredContent, but under a long instructions string rather than a dedicated field.
- One change: add a top-level structuredContent.receipt_url field (plus issued_at), so clients and verifiers can read it without parsing the prose instructions.
- Receipt: https://runx.ai/r/1fdaa455887d7dff3ee4e5793f71a50319fe886fb9746c93bc91d46698a3855f
