<script lang="ts">
  import { onMount } from 'svelte';

  let currentTime = $state<Date | null>(null);

  onMount(() => {
    const updateTime = () => {
      currentTime = new Date();
    };

    updateTime();

    const timer = setInterval(updateTime, 1000);

    return () => clearInterval(timer);
  });

  const dateFormatter = new Intl.DateTimeFormat('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
    year: 'numeric'
  });

  const timeFormatter = new Intl.DateTimeFormat('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    second: '2-digit',
    hour12: true
  });

  const greeting = $derived(
    currentTime === null
      ? 'Welcome to DayReign'
      : currentTime.getHours() < 12
        ? 'Good morning'
        : currentTime.getHours() < 17
          ? 'Good afternoon'
          : 'Good evening'
  );
</script>

<svelte:head>
  <title>DayReign | Command Your Day</title>
</svelte:head>

<div class="min-h-screen bg-[#F5F0E6] text-[#292524]">

  <!-- Navigation -->
  <header class="border-b border-[#D9C9AE] bg-[#FFFDF8]">
    <nav
      class="mx-auto flex max-w-7xl items-center
             justify-between px-6 py-5"
    >
      <div class="flex items-center gap-3">
        <span class="text-3xl text-[#8E2028]">❦</span>
        <h1 class="font-serif text-2xl font-bold
                   tracking-widest text-[#8E2028]">
          DAYREIGN
        </h1>
      </div>

      <span class="hidden text-sm tracking-widest
                   text-[#9A793F] sm:block">
        TEMPUS REGIT ACTUM
      </span>
    </nav>
  </header>

  <main class="mx-auto max-w-7xl space-y-8 px-6 py-10">

    <!-- Imperial hero -->
    <section
      class="rounded-2xl bg-[#8E2028] p-8
             text-[#FFF8EB] shadow-lg md:p-12"
    >
      <p class="mb-3 text-xs font-semibold
                tracking-[0.25em] text-[#E5C47A]">
        YOUR IMPERIAL DASHBOARD
      </p>

      <h2 class="font-serif text-4xl md:text-5xl">
        {greeting}.
      </h2>

      <p class="mt-3 text-lg text-[#F3D9D3]">
        Command your day. Shape your future.
      </p>

      <div
        class="mt-8 flex flex-col gap-5
               border-t border-[#C07878] pt-6
               md:flex-row md:items-end
               md:justify-between"
      >
        <div>
          <p class="text-sm text-[#E5C47A]">
            TODAY'S DATE
          </p>

          <p class="mt-2 font-serif text-xl">
            {currentTime
              ? dateFormatter.format(currentTime)
              : 'Loading...'}
          </p>
        </div>

        <div>
          <p class="text-sm text-[#E5C47A]">
            LOCAL TIME
          </p>

          <p class="mt-2 text-2xl font-semibold
                    tabular-nums">
            {currentTime
              ? timeFormatter.format(currentTime)
              : '--:--:--'}
          </p>
        </div>
      </div>
    </section>

    <!-- Dashboard sections -->
    <section class="grid gap-6 md:grid-cols-2">

      <!-- Today -->
      <article
        class="rounded-2xl border border-[#E0D3BE]
               bg-[#FFFDF8] p-7 shadow-sm"
      >
        <div class="mb-5 flex items-center justify-between">
          <h3 class="font-serif text-2xl text-[#8E2028]">
            Today's Agenda
          </h3>
          <span class="text-2xl text-[#C6A052]">☀</span>
        </div>

        <div class="mb-5 h-px bg-[#E6D5B8]"></div>

        <p class="text-[#766C60]">
          No events scheduled for today.
        </p>
      </article>

      <!-- This Week -->
      <article
        class="rounded-2xl border border-[#E0D3BE]
               bg-[#FFFDF8] p-7 shadow-sm"
      >
        <div class="mb-5 flex items-center justify-between">
          <h3 class="font-serif text-2xl text-[#8E2028]">
            The Week Ahead
          </h3>
          <span class="text-2xl text-[#C6A052]">❦</span>
        </div>

        <div class="mb-5 h-px bg-[#E6D5B8]"></div>

        <p class="text-[#766C60]">
          Your upcoming events will appear here.
        </p>
      </article>
    </section>

    <!-- Calendar -->
    <section
      class="rounded-2xl border border-[#E0D3BE]
             bg-[#FFFDF8] p-7 shadow-sm"
    >
      <div class="mb-6 flex flex-wrap
                  items-center justify-between gap-4">
        <div>
          <p class="mb-2 text-xs tracking-widest
                    text-[#B28B46]">
            YOUR IMPERIAL CALENDAR
          </p>

          <h3 class="font-serif text-3xl text-[#8E2028]">
            Monthly Overview
          </h3>
        </div>

        <span class="rounded-lg bg-[#F5F0E6]
                     px-4 py-2 text-sm text-[#8E2028]">
          Calendar coming next
        </span>
      </div>

      <div class="h-px bg-[#E6D5B8]"></div>

      <div class="py-16 text-center">
        <div class="mb-4 text-5xl text-[#C6A052]">
          ❦
        </div>

        <p class="font-serif text-xl text-[#365747]">
          Every great day begins with a plan.
        </p>

        <p class="mt-2 text-sm text-[#766C60]">
          Your interactive calendar will live here.
        </p>
      </div>
    </section>

  </main>

  <footer class="py-8 text-center text-sm text-[#897C6C]">
    DAYREIGN · TEMPUS REGIT ACTUM
  </footer>
</div>
