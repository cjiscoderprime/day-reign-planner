<script lang="ts">
    import EventForm from '#lib/components/EventForm.svelte';
    import type {
      CalendarEvent,
      EventInput
    } from '#lib/types/event.ts';
    import Calendar from '#lib/components/Calendar.svelte';

    import { onMount } from 'svelte';

    let selectedDate = $state('');

    let currentTime = $state<Date | null>(null);

    let events = $state<CalendarEvent[]>([]);
    let showEventForm = $state(false);
    let editingEvent = $state<CalendarEvent | null>(null);

    const todayEvents = $derived.by(() => {
    if (!currentTime) return [];

    const today = localDateKey(currentTime);

    return events
      .filter((event) => event.date === today)
      .sort(compareEvents);
    });

    const weekEvents = $derived.by(() => {
      if (!currentTime) return [];

    const monday = new Date(currentTime);
    monday.setHours(12, 0, 0, 0);

    const offset = (monday.getDay() + 6) % 7;
    monday.setDate(monday.getDate() - offset);

    const sunday = new Date(monday);
    sunday.setDate(monday.getDate() + 6);

    const start = localDateKey(monday);
    const end = localDateKey(sunday);

    return events
      .filter((event) => event.date >= start && event.date <= end)
      .sort((a, b) =>
        a.date.localeCompare(b.date) || compareEvents(a, b)
      );
    });

    function compareEvents(a: CalendarEvent, b: CalendarEvent) {
      if (a.allDay !== b.allDay) {
        return a.allDay ? -1 : 1;
      }

      return a.startTime.localeCompare(b.startTime);
    }

    function openCreateEvent() {
      editingEvent = null;
      showEventForm = true;
    }

    function deleteEvent(id: string) {
      const confirmed = window.confirm(
        'Are you sure you want to delete this event?'
      );

      if (!confirmed) return;

      events = events.filter((event) => event.id !== id);
    }

    function localDateKey(date: Date): string {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');

      return `${year}-${month}-${day}`;
  }

    function closeEventForm() {
      showEventForm = false;
      editingEvent = null;
    }

    function saveEvent(input: EventInput) {
      if (editingEvent) {
        events = events.map((event) =>
          event.id === editingEvent?.id
            ? { ...input, id: event.id }
            : event
        );
      } else {
        events = [
          ...events,
          {
            ...input,
            id: crypto.randomUUID()
          }
        ];
      }

      closeEventForm();
    }

    function editEvent(event: CalendarEvent) {
      editingEvent = event;
      showEventForm = true;
    }

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
      <div class="flex justify-end">
      <button
        onclick={openCreateEvent}
        class="rounded-xl bg-[#8E2028] px-6 py-3
              font-semibold text-white shadow-md
              transition hover:bg-[#741920]"
      >
        + Add Event
      </button>
    </div>

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

          {#each todayEvents as event (event.id)}
          <div class="mb-3 rounded-xl bg-[#F8F3E9] p-4">
            <p class="font-semibold text-[#8E2028]">
              {event.title}
            </p>

            <p class="mt-1 text-sm text-[#766C60]">
              {event.allDay
                ? 'All day'
                : `${event.startTime} – ${event.endTime}`}
              · {event.category}
            </p>
          </div>
          {:else}
            <p class="text-[#766C60]">
              No events scheduled for today.
            </p>
          {/each}
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

          {#each weekEvents as event (event.id)}
          <div class="mb-3 rounded-xl bg-[#F8F3E9] p-4">
            <p class="font-semibold text-[#8E2028]">
              {event.title}
            </p>

            <p class="mt-1 text-sm text-[#766C60]">
              {event.date}
              · {event.allDay ? 'All day' : event.startTime}
              · {event.category}
            </p>
          </div>
            {:else}
              <p class="text-[#766C60]">
                No events scheduled this week.
              </p>
            {/each}

        </article>
      </section>

      <!-- Calendar -->
      <Calendar bind:selectedDate {events}/>

      <section
      class="rounded-2xl border border-[#E0D3BE]
            bg-[#FFFDF8] p-7 shadow-sm"
      >
      <h3 class="mb-4 font-serif text-2xl text-[#8E2028]">
        Events for Selected Date
      </h3>

      {#each events.filter((event) => event.date === selectedDate) as event (event.id)}
        <div
          class="mb-3 flex items-center justify-between gap-4
                rounded-xl border border-[#E6D5B8] p-4"
        >
          <div>
            <h4 class="font-semibold text-[#292524]">
              {event.title}
            </h4>

            <p class="mt-1 text-sm text-[#766C60]">
              {event.allDay
                ? 'All day'
                : `${event.startTime} – ${event.endTime}`}
              · {event.category}
            </p>

            {#if event.description}
              <p class="mt-2 text-sm text-[#766C60]">
                {event.description}
              </p>
            {/if}
          </div>

          <div class = "flex gap-2">

            <button
              onclick={() => editEvent(event)}
              class = "rounded-lg border border-[#C6A052]
              px-4 py-2 text-sm text-[#8E2028]  hover:bg-[#F5F0E6]">
              Edit
            </button>

            <button
              onclick={() => deleteEvent(event.id)}
              class="rounded-lg border border-[#E7B5B5]
                    px-4 py-2 text-sm text-[#A32630]
                    hover:bg-[#FFF0F0]"
              >
                Delete
            </button>

          </div>
        </div>
      {:else}
        <p class="text-sm text-[#766C60]">
          No events scheduled for this date.
        </p>
      {/each}
    </section>

    </main>

    <footer class="py-8 text-center text-sm text-[#897C6C]">
      DAYREIGN · TEMPUS REGIT ACTUM
    </footer>
  </div>

  {#if showEventForm}
  {#key editingEvent?.id ?? 'new'}
    <EventForm
      selectedDate={selectedDate || localDateKey(new Date)}
      {editingEvent}
      onSave={saveEvent}
      onCancel={closeEventForm}
    />
  {/key}
{/if}