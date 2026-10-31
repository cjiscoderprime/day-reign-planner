<script lang="ts">

import type { CalendarEvent } from '#lib/types/event.ts';

const weekdays = [
    'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'
];

function formatDate(date: Date): string {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');

    return `${year}-${month}-${day}`;
}

const eventCounts = $derived.by(() => {
  const counts: Record<string, number> = {};

  for (const event of events) {
    counts[event.date] = (counts[event.date] ?? 0) + 1;
  }

  return counts;
});

const today = new Date();

let {
    selectedDate = $bindable(formatDate(today)),
    events = []
}: {
    selectedDate?: string;
    events?: CalendarEvent[];
} = $props();

let currentMonth = $state(
    new Date(today.getFullYear(), today.getMonth(), 1)
);

const monthTitle = $derived(
    currentMonth.toLocaleDateString('en-US', {
        month: 'long',
        year: 'numeric',
    })
);

const selectedDateLabel = $derived(
    new Date(`${selectedDate}T12:00:00`).toLocaleDateString(
        'en-US',
        {
            weekday: 'long',
            month: 'long',
            day: 'numeric',
            year: 'numeric'
        }
    )
);

const calendarDays = $derived.by(() => {
    const year = currentMonth.getFullYear();
    const month = currentMonth.getMonth();

    const firstDay = new Date(year, month, 1);

    //Convert Javascript's Sunday-first indexing to Monday-first
    const startingOffset = (firstDay.getDay() + 6) % 7;

      const daysInMonth = new Date(year, month + 1, 0).getDate();

    const totalCells =
      Math.ceil((startingOffset + daysInMonth) / 7) * 7;

    return Array.from({ length: totalCells }, (_, index) => {
      const date = new Date(
        year,
        month,
        index - startingOffset + 1
      );

      return {
        date: formatDate(date),
        day: date.getDate(),
        inCurrentMonth: date.getMonth() === month
      };
    });
  });

  function changeMonth(amount: number) {
    currentMonth = new Date(
      currentMonth.getFullYear(),
      currentMonth.getMonth() + amount,
      1
    );
  }

  function goToToday() {
    const now = new Date();

    currentMonth = new Date(
      now.getFullYear(),
      now.getMonth(),
      1
    );

    selectedDate = formatDate(now);
  }

  function selectDate(date: string) {
    selectedDate = date;

    const [year, month] = date.split('-').map(Number);

    if (
      year !== currentMonth.getFullYear() ||
      month !== currentMonth.getMonth() + 1
    ) {
      currentMonth = new Date(year, month - 1, 1);
    }
  }
</script>

<section
  class="rounded-2xl border border-[#E0D3BE]
         bg-[#FFFDF8] p-5 shadow-sm md:p-8"
>
  <!-- Calendar header -->
  <div
    class="mb-7 flex flex-wrap items-center
           justify-between gap-4"
  >
    <div>
      <p
        class="mb-2 text-xs font-semibold
               tracking-[0.2em] text-[#B28B46]"
      >
        THE IMPERIAL CALENDAR
      </p>

      <h2 class="font-serif text-3xl text-[#8E2028]">
        {monthTitle}
      </h2>
    </div>

    <div class="flex items-center gap-2">
      <button
        onclick={goToToday}
        class="rounded-lg border border-[#D9C9AE]
               px-4 py-2 text-sm text-[#8E2028]
               transition hover:bg-[#F5F0E6]"
      >
        Today
      </button>

      <button
        onclick={() => changeMonth(-1)}
        aria-label="Previous month"
        class="rounded-lg border border-[#D9C9AE]
               px-4 py-2 hover:bg-[#F5F0E6]"
      >
        ‹
      </button>

      <button
        onclick={() => changeMonth(1)}
        aria-label="Next month"
        class="rounded-lg border border-[#D9C9AE]
               px-4 py-2 hover:bg-[#F5F0E6]"
      >
        ›
      </button>
    </div>
  </div>

  <!-- Weekday labels -->
  <div class="grid grid-cols-7 gap-1 md:gap-2">
    {#each weekdays as weekday}
      <div
        class="py-3 text-center text-xs font-semibold
              uppercase tracking-wider text-[#9A793F]"
      >
        {weekday}
      </div>
    {/each}

    <!-- Calendar dates -->
    {#each calendarDays as date (date.date)}
      {@const isToday = date.date === formatDate(new Date())}
      {@const isSelected = date.date === selectedDate}

      <button
        onclick={() => selectDate(date.date)}
        aria-label={`Select ${date.date}`}
        aria-pressed={isSelected}
        aria-current={isToday ? 'date' : undefined}
        class={[
          'relative flex min-h-14 items-center justify-center',
          'rounded-xl border text-sm transition-all',
          'md:min-h-20 md:text-base',
          isSelected
            ? 'border-[#8E2028] bg-[#8E2028] font-bold text-white shadow-md'
            : isToday
              ? 'border-[#C6A052] bg-[#FAF2DE] font-bold text-[#8E2028]'
              : 'border-transparent hover:border-[#E6D5B8] hover:bg-[#F5F0E6]',
          !date.inCurrentMonth && !isSelected
            ? 'text-[#BDB4A6]'
            : !isSelected && !isToday
              ? 'text-[#514943]'
              : ''
        ].join(' ')}
      >
        {date.day}

        {#if eventCounts[date.date]}
        <span
          class={[
            'absolute right-1 top-1 flex h-5 min-w-5',
            'items-center justify-center rounded-full',
            'px-1 text-[10px] font-semibold',
            isSelected
              ? 'bg-white text-[#8E2028]'
              : 'bg-[#C6A052] text-white'
          ].join(' ')}
        >
          {eventCounts[date.date]}
        </span>
        {/if}

        {#if isToday}
          <span
            class={[
              'absolute bottom-2 h-1.5 w-1.5 rounded-full',
              isSelected ? 'bg-white' : 'bg-[#8E2028]'
            ].join(' ')}
          ></span>
        {/if}
      </button>
    {/each}
  </div>

  <!-- Selected date -->
  <div
    class="mt-7 rounded-xl border border-[#E6D5B8]
           bg-[#F8F3E9] p-5"
  >
    <p class="mb-2 text-xs font-semibold
              tracking-widest text-[#B28B46]">
      SELECTED DATE
    </p>

    <h3 class="font-serif text-xl text-[#8E2028]">
      {selectedDateLabel}
    </h3>

    <p class="mt-2 text-sm text-[#766C60]">
      Events for this date will appear here.
    </p>
  </div>
</section>
