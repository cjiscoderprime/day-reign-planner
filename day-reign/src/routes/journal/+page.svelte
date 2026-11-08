
<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { api } from '#lib/api.ts';

  import type {
    Memory,
    MemoryInput
  } from '#lib/types/memory.ts';

  let memories = $state<Memory[]>([]);
  let loading = $state(true);
  let saving = $state(false);
  let error = $state('');
  let editingId = $state<string | null>(null);

  function todayKey(): string {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');

    return `${year}-${month}-${day}`;
  }

  let title = $state('');
  let date = $state(todayKey());
  let content = $state('');

  let search = $state('');

  const filteredMemories = $derived(
    memories.filter((memory) => {
      const query = search.toLowerCase().trim();

      return (
        memory.title.toLowerCase().includes(query) ||
        memory.content.toLowerCase().includes(query) ||
        memory.date.includes(query)
      );
    })
  );

  onMount(() => {
    async function initialize() {
      try {
        await api.me();
        memories = await api.getMemories();
      } catch (err) {
        if (
          err instanceof Error &&
          (
            err.message === 'Not authenticated' ||
            err.message === 'Session expired or invalid'
          )
        ) {
          await goto('/');
          return;
        }

        error = err instanceof Error
          ? err.message
          : 'Could not load journal';
      } finally {
        loading = false;
      }
    }

    void initialize();
  });

  function clearEditor() {
    title = '';
    date = todayKey();
    content = '';
    editingId = null;
    error = '';
  }

  function editMemory(memory: Memory) {
    editingId = memory.id;
    title = memory.title;
    date = memory.date;
    content = memory.content;

    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  }

  async function saveMemory() {
    if (saving) return;

    if (!title.trim() || !content.trim()) {
      error = 'Please enter a title and journal entry.';
      return;
    }

    const input: MemoryInput = {
      title: title.trim(),
      date,
      content: content.trim()
    };

    saving = true;
    error = '';

    try {
      if (editingId) {
        const updated = await api.updateMemory(
          editingId,
          input
        );

        memories = memories.map((memory) =>
          memory.id === updated.id ? updated : memory
        );
      } else {
        const created = await api.createMemory(input);
        memories = [created, ...memories];
      }

      memories = [...memories].sort((a, b) =>
        b.date.localeCompare(a.date) ||
        b.createdAt.localeCompare(a.createdAt)
      );

      clearEditor();
    } catch (err) {
      error = err instanceof Error
        ? err.message
        : 'Could not save memory';
    } finally {
      saving = false;
    }
  }

  async function deleteMemory(id: string) {
    if (!window.confirm('Permanently delete this memory?')) {
      return;
    }

    error = '';

    try {
      await api.deleteMemory(id);

      memories = memories.filter((memory) =>
        memory.id !== id
      );

      if (editingId === id) {
        clearEditor();
      }
    } catch (err) {
      error = err instanceof Error
        ? err.message
        : 'Could not delete memory';
    }
  }
</script>

<svelte:head>
  <title>Memory Journal | DayReign</title>
</svelte:head>

<div class="min-h-screen bg-[#F5F0E6] text-[#292524]">

  <header class="border-b border-[#D9C9AE] bg-[#FFFDF8]">
    <nav
      class="mx-auto flex max-w-7xl items-center
             justify-between gap-4 px-6 py-5"
    >
      <a href="/" class="flex items-center gap-3">
        <span class="text-3xl">🏛️</span>
        <span
          class="font-serif text-2xl font-bold
                 tracking-widest text-[#8E2028]"
        >
          DAYREIGN
        </span>
      </a>

      <a
        href="/"
        class="rounded-lg border border-[#C6A052]
               px-4 py-2 text-sm text-[#8E2028]
               hover:bg-[#F5F0E6]"
      >
        Back to Dashboard
      </a>
    </nav>
  </header>

  <main class="mx-auto max-w-5xl space-y-8 px-6 py-10">

    <section
      class="rounded-2xl bg-[#8E2028]
             p-8 text-[#FFF8EB] shadow-lg md:p-12"
    >
      <p
        class="mb-3 text-xs font-semibold
               tracking-[0.25em] text-[#E5C47A]"
      >
        DAYREIGN · PERSONAL CHRONICLES
      </p>

      <h1 class="font-serif text-4xl md:text-5xl">
        Memory Journal
      </h1>

      <p class="mt-4 text-[#F3D9D3]">
        Preserve your thoughts, lessons, and moments
        worth remembering.
      </p>
    </section>

    {#if error}
      <div
        role="alert"
        class="rounded-xl border border-red-300
               bg-red-50 p-4 text-red-800"
      >
        {error}
      </div>
    {/if}

    {#if loading}
      <p class="text-[#8E2028]">
        Opening your chronicles...
      </p>
    {:else}
      <section
        class="rounded-2xl border border-[#E0D3BE]
               bg-[#FFFDF8] p-7 shadow-sm"
      >
        <div class="mb-6 flex items-center justify-between">
          <div>
            <p
              class="text-xs font-semibold uppercase
                     tracking-widest text-[#9A793F]"
            >
              Your personal chronicle
            </p>

            <h2
              class="mt-2 font-serif text-2xl text-[#8E2028]"
            >
              {editingId ? 'Edit Memory' : 'Add Memory'}
            </h2>
          </div>

          <span class="text-3xl text-[#C6A052]">✍</span>
        </div>

        <form
          class="space-y-5"
          onsubmit={(event) => {
            event.preventDefault();
            void saveMemory();
          }}
        >
          <div>
            <label
              for="memory-title"
              class="mb-2 block text-sm font-semibold"
            >
              Title
            </label>

            <input
              id="memory-title"
              type="text"
              bind:value={title}
              maxlength="150"
              required
              placeholder="What will you remember about today?"
              class="w-full rounded-xl border border-[#D9C9AE]
                     bg-[#FFFEFB] p-3 outline-none
                     focus:border-[#8E2028]"
            />
          </div>

          <div>
            <label
              for="memory-date"
              class="mb-2 block text-sm font-semibold"
            >
              Date
            </label>

            <input
              id="memory-date"
              type="date"
              bind:value={date}
              required
              class="rounded-xl border border-[#D9C9AE]
                     bg-[#FFFEFB] p-3"
            />
          </div>

          <div>
            <label
              for="memory-content"
              class="mb-2 block text-sm font-semibold"
            >
              Your Reflection
            </label>

            <textarea
              id="memory-content"
              bind:value={content}
              maxlength="30000"
              rows="14"
              required
              placeholder="What happened today? What did you learn? What would you like to remember?"
              class="w-full resize-y rounded-xl
                     border border-[#D9C9AE]
                     bg-[#FFFEFB] p-4 leading-7
                     outline-none focus:border-[#8E2028]"
            ></textarea>

            <p class="mt-2 text-right text-xs text-[#766C60]">
              {content.length.toLocaleString()} / 30,000 characters
            </p>
          </div>

          <div class="flex flex-wrap gap-3">
            <button
              type="submit"
              disabled={saving}
              class="rounded-xl bg-[#8E2028]
                     px-6 py-3 font-semibold text-white
                     hover:bg-[#741920]
                     disabled:opacity-50"
            >
              {saving
                ? 'Saving...'
                : editingId
                  ? 'Update Memory'
                  : 'Save Memory'}
            </button>

            {#if editingId}
              <button
                type="button"
                onclick={clearEditor}
                class="rounded-xl border border-[#C6A052]
                       px-6 py-3 text-[#8E2028]"
              >
                Cancel Editing
              </button>
            {/if}
          </div>
        </form>
      </section>

      <section class="space-y-5">
        <div
          class="flex flex-wrap items-center
                 justify-between gap-4"
        >
          <div>
            <h2 class="font-serif text-3xl text-[#8E2028]">
              Your Chronicles
            </h2>

            <p class="mt-1 text-sm text-[#766C60]">
              {memories.length} saved memories
            </p>
          </div>

          <input
            type="search"
            bind:value={search}
            placeholder="Search your memories..."
            aria-label="Search your memories"
            class="rounded-xl border border-[#D9C9AE]
                   bg-[#FFFDF8] p-3 text-sm"
          />
        </div>

        {#each filteredMemories as memory (memory.id)}
          <article
            class="rounded-2xl border border-[#E0D3BE]
                   bg-[#FFFDF8] p-6 shadow-sm"
          >
            <p
              class="text-xs font-semibold uppercase
                     tracking-wider text-[#9A793F]"
            >
              {memory.date}
            </p>

            <h3
              class="mt-2 font-serif text-2xl text-[#8E2028]"
            >
              {memory.title}
            </h3>

            <p
              class="mt-4 whitespace-pre-wrap break-words
                     text-sm leading-7 text-[#514943]"
            >
              {memory.content}
            </p>

            <div
              class="mt-6 flex gap-3 border-t
                     border-[#E6D5B8] pt-4"
            >
              <button
                type="button"
                onclick={() => editMemory(memory)}
                class="rounded-lg border border-[#C6A052]
                       px-4 py-2 text-sm text-[#8E2028]"
              >
                Edit
              </button>

              <button
                type="button"
                onclick={() => void deleteMemory(memory.id)}
                class="rounded-lg border border-[#E7B5B5]
                       px-4 py-2 text-sm text-[#A32630]"
              >
                Delete
              </button>
            </div>
          </article>
        {:else}
          <div
            class="rounded-2xl border border-[#E0D3BE]
                   bg-[#FFFDF8] p-10 text-center
                   text-[#766C60]"
          >
            {search
              ? 'No memories match your search.'
              : 'Your chronicles begin with your first memory.'}
          </div>
        {/each}
      </section>
    {/if}
  </main>

  <footer class="py-8 text-center text-sm text-[#897C6C]">
    DAYREIGN · TEMPUS REGIT ACTUM
  </footer>
</div>

