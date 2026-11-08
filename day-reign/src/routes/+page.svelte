<script lang="ts">
    import Calendar from '#lib/components/Calendar.svelte';
    import { onMount } from 'svelte';
    import EventForm from '#lib/components/EventForm.svelte';
    import AuthForm from '#lib/components/AuthForm.svelte';
    import { api, type AuthUser } from '#lib/api.ts';

    import type {
      CalendarEvent,
      EventInput
    } from '#lib/types/event.ts';

    let user = $state<AuthUser | null>(null);
    let authLoading = $state(true);
    let eventsLoading = $state(false);
    let saving = $state(false);
    let apiError = $state('');

    let selectedDate = $state(localDateKey(new Date()));

    let currentTime = $state<Date | null>(null);

    let events = $state<CalendarEvent[]>([]);
    let showEventForm = $state(false);
    let editingEvent = $state<CalendarEvent | null>(null);
    
    let showNextWeek = $state(false);
    let showThisMonth = $state(false);

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

  const nextWeekEvents = $derived.by(() => {
    if (!currentTime) return [];

    const monday = new Date(currentTime);
    monday.setHours(12, 0, 0, 0);

    const offset = (monday.getDay() + 6) % 7;
    monday.setDate(monday.getDate() - offset + 7);

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

  const monthEvents = $derived.by(() => {
    if (!currentTime) return [];

    const year = currentTime.getFullYear();
    const month = currentTime.getMonth();

    const start = localDateKey(new Date(year, month, 1));
    const end = localDateKey(new Date(year, month + 1, 0));

    return events
      .filter((event) => event.date >= start && event.date <= end)
      .sort((a, b) =>
        a.date.localeCompare(b.date) || compareEvents(a, b)
      );
  });

  async function handleAuthenticated(account: AuthUser) {
    user = account;
    await loadEvents();
  }

  async function logout() {
    try {
      await api.logout();
      user = null;
      events = [];
    } catch (error) {
      apiError = error instanceof Error
        ? error.message
        : 'Could not log out';
    }
  }

    function compareEvents(a: CalendarEvent, b: CalendarEvent) {
      if (a.allDay !== b.allDay) {
        return a.allDay ? -1 : 1;
      }

      return a.startTime.localeCompare(b.startTime);
    }

    async function loadEvents() {
      eventsLoading = true;
      apiError = '';

      try {
        events = await api.getEvents();
      } catch (error) {
        apiError = error instanceof Error
          ? error.message
          : 'Could not load events';
      } finally {
        eventsLoading = false;
      }
    }

    function openCreateEvent() {
      editingEvent = null;
      showEventForm = true;
    }

    async function deleteEvent(id: string) {
      if (!window.confirm('Delete this event?')) return;

      apiError = '';

      try {
        await api.deleteEvent(id);
        events = events.filter((event) => event.id !== id);
      } catch (error) {
        apiError = error instanceof Error
          ? error.message
          : 'Could not delete event';
      }
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

    async function saveEvent(input: EventInput) {
      if (saving) return;
      saving = true;
      apiError = '';

      try {
        if (editingEvent) {
          const updated = await api.updateEvent(
            editingEvent.id,
            input
          );

          events = events.map((event) =>
            event.id === updated.id ? updated : event
          );
        } else {
          const created = await api.createEvent(input);

          events = [...events, created];
        }

        closeEventForm();
      } catch (error) {
        apiError = error instanceof Error
          ? error.message
          : 'Could not save event';
      } finally {
        saving = false;
      }
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

    onMount(() => {
      async function restoreSession() {
        try {
          user = await api.me();
        } catch {
          user = null;
        } finally {
          authLoading = false;
        }
        if (user) {
          await loadEvents();
        }
      }
      void restoreSession();
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

  {#if authLoading}
    <div class="flex min-h-screen items-center justify-center bg-[#F5F0E6]">
      <p class="font-serif text-2xl text-[#8E2028]">
        Opening DayReign...
      </p>
    </div>

  {:else if !user}
    <AuthForm onAuthenticated={handleAuthenticated} />

  {:else}

  <div class="min-h-screen bg-[#F5F0E6] text-[#292524]">

    <!-- Navigation -->
    <header class="border-b border-[#D9C9AE] bg-[#FFFDF8]">
      <nav
        class="mx-auto flex max-w-7xl items-center
              justify-between px-6 py-5"
      >
        <div class="flex items-center gap-3">
          <span class="text-3xl text-[#8E2028]">🏛️</span>
          <h1 class="font-serif text-2xl font-bold
                    tracking-widest text-[#8E2028]">
            DAYREIGN
          </h1>
        </div>

        <span class="hidden text-sm tracking-widest
                    text-[#9A793F] sm:block">
          TEMPUS REGIT ACTUM
        </span>

        <a
          href="/journal"
          class="rounded-lg bg-[#8E2028]
                px-4 py-2 text-sm font-semibold
                text-white transition
                hover:bg-[#741920]"
          >
          + Add Memory
        </a>

         <button
          onclick={logout}
          class="rounded-lg border border-[#C6A052]
                px-4 py-2 text-sm text-[#8E2028]
                hover:bg-[#F5F0E6]">
          Sign Out
        </button>

      </nav>
    </header>

    <main class="mx-auto max-w-7xl space-y-8 px-6 py-10">

      {#if apiError}
      <div
        role="alert"
        class="rounded-xl border border-red-300
        bg-red-50 p-4 text-red-800">
          {apiError}
      </div>
      {/if}

      {#if eventsLoading}
        <p class="text-[#8E2028]">
          Loading your events...
        </p>
      {/if}

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
              This Week
            </h3>
            <span class="text-2xl text-[#C6A052]">🏛️</span>
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

      
      <!-- Optional dashboard sections -->
      <section class="space-y-5">

        <div
          class="flex flex-wrap items-center justify-between
                gap-4 rounded-2xl border border-[#E0D3BE]
                bg-[#FFFDF8] p-5 shadow-sm"
        >
          <div>
            <h3 class="font-serif text-xl text-[#8E2028]">
              Customize Your Overview
            </h3>
            <p class="mt-1 text-sm text-[#766C60]">
              Choose which additional schedules to display.
            </p>
          </div>

          <div class="flex flex-wrap gap-5">

            <label class="flex cursor-pointer items-center gap-3">
              <span class="text-sm font-medium text-[#514943]">
                Next Week
              </span>
              <input
                type="checkbox"
                role="switch"
                bind:checked={showNextWeek}
                class="h-5 w-5 accent-[#8E2028]"
              />
            </label>

            <label class="flex cursor-pointer items-center gap-3">
              <span class="text-sm font-medium text-[#514943]">
                This Month
              </span>
              <input
                type="checkbox"
                role="switch"
                bind:checked={showThisMonth}
                class="h-5 w-5 accent-[#8E2028]"
              />
            </label>

          </div>
        </div>

        {#if showNextWeek || showThisMonth}
          <div class="grid gap-6 md:grid-cols-2">

            {#if showNextWeek}
              <article
                class="rounded-2xl border border-[#E0D3BE]
                      bg-[#FFFDF8] p-7 shadow-sm"
              >
                <h3 class="mb-5 font-serif text-2xl text-[#8E2028]">
                  Next Week
                </h3>

                <div class="mb-5 h-px bg-[#E6D5B8]"></div>

                {#each nextWeekEvents as event (event.id)}
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
                  <p class="text-sm text-[#766C60]">
                    No events scheduled for next week.
                  </p>
                {/each}
              </article>
            {/if}

            {#if showThisMonth}
              <article
                class="rounded-2xl border border-[#E0D3BE]
                      bg-[#FFFDF8] p-7 shadow-sm"
              >
                <h3 class="mb-5 font-serif text-2xl text-[#8E2028]">
                  This Month
                </h3>

                <div class="mb-5 h-px bg-[#E6D5B8]"></div>

                {#each monthEvents as event (event.id)}
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
                  <p class="text-sm text-[#766C60]">
                    No events scheduled this month.
                  </p>
                {/each}
              </article>
            {/if}

          </div>
        {/if}

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
      selectedDate={selectedDate || localDateKey(new Date())}
      {editingEvent}
      onSave={saveEvent}
      onCancel={closeEventForm}
    />
  {/key}
{/if}
{/if}