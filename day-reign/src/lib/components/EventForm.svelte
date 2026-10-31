<script lang="ts">
    import type {
        CalendarEvent,
        EventCategory,
        EventInput
    } from '#lib/types/event.ts';

    interface Props {
        selectedDate: string;
        editingEvent?: CalendarEvent | null;
        onSave: (event: EventInput) => void | Promise<void>;
        onCancel: () => void;
    }

    let {
        selectedDate,
        editingEvent = null,
        onSave,
        onCancel
    }: Props = $props();

    const categories: EventCategory[] = [
        'Personal',
        'School',
        'Work',
        'Health',
        'Other'
    ];


        
    let title = $state('');
    let date = $state('');
    let startTime = $state('09:00');
    let endTime = $state('10:00');
    let allDay = $state(false);
    let category = $state<EventCategory>('Personal');
    let description = $state('');
    let error = $state('');

    function initializeForm() {
        title = editingEvent?.title ?? '';
        date = editingEvent?.date ?? selectedDate;
        startTime = editingEvent?.startTime || '09:00';
        endTime = editingEvent?.endTime || '10:00';
        allDay = editingEvent?.allDay ?? false;
        category = editingEvent?.category ?? 'Personal';
        description = editingEvent?.description ?? '';
        error = '';
    }

    $effect(() => {
        const eventToEdit = editingEvent;
        const initialDate = selectedDate;

        title = eventToEdit?.title ?? '';
        date = eventToEdit?.date ?? initialDate;
        startTime = eventToEdit?.startTime || '09:00';
        endTime = eventToEdit?.endTime || '10:00';
        allDay = eventToEdit?.allDay ?? false;
        category = eventToEdit?.category ?? 'Personal';
        description = eventToEdit?.description ?? '';
        error = '';
    });

    function submitEvent(event: SubmitEvent) {
        event.preventDefault();
        error = '';

        if (!title.trim()) {
            error = 'Please enter an event title.';
            return;
        }

        if (!date) {
            error = 'Please select a date.';
            return;
        }

        if (!allDay && endTime <= startTime) {
            error = 'End time must be later than start time.';
            return;
        }

        onSave({
            title: title.trim(),
            date,
            startTime: allDay ? '' : startTime,
            endTime: allDay ? '' : endTime,
            allDay,
            category,
            description: description.trim()
        });
    } 
</script>

<div
    class="fixed inset-0 z-50 flex items-center justify-center
            bg-black/40 p-4"
    role="presentation"
>
    <div
    role="dialog"
    aria-modal="true"
    aria-labelledby="event-form-title"
    class="w-full max-w-lg overflow-y-auto rounded-2xl
           border border-[#D9C9AE] bg-[#FFFDF8]
           p-6 shadow-2xl max-h-[90vh] md:p-8"
    >
    <div class="mb-6 flex items-start justify-between gap-4">
        <div>
            <p class="text-xs font-semibold tracking-[0.2em]
                    text-[#B28B46]">
            DAYREIGN · IMPERIAL PLANNER
            </p>

            <h2
            id="event-form-title"
            class="mt-2 font-serif text-3xl text-[#8E2028]"
            >
            {editingEvent ? 'Edit Event' : 'Create Event'}
            </h2>
        </div>

        <button
            type="button"
            onclick={onCancel}
            aria-label="Close form"
            class="rounded-lg p-2 text-[#8E2028]
                hover:bg-[#F5F0E6]"
        >
            ✕
        </button>
        </div>

        <form onsubmit={submitEvent} class="space-y-5">
        <div>
            <label for="event-title" class="mb-2 block text-sm font-medium">
            Event title
            </label>
            <input
            id="event-title"
            type="text"
            bind:value={title}
            maxlength="120"
            required
            placeholder="e.g. Project meeting"
            class="w-full rounded-lg border border-[#D9C9AE]
                    bg-white px-4 py-3 outline-none
                    focus:border-[#8E2028]"
            />
        </div>

        <div>
            <label for="event-date" class="mb-2 block text-sm font-medium">
            Date
            </label>
            <input
            id="event-date"
            type="date"
            bind:value={date}
            required
            class="w-full rounded-lg border border-[#D9C9AE]
                    bg-white px-4 py-3 outline-none
                    focus:border-[#8E2028]"
            />
        </div>

        <label class="flex items-center gap-3 text-sm">
            <input
            type="checkbox"
            bind:checked={allDay}
            class="h-4 w-4 accent-[#8E2028]"
            />
            All-day event
        </label>

        {#if !allDay}
            <div class="grid grid-cols-2 gap-4">
            <div>
                <label for="event-start" class="mb-2 block text-sm font-medium">
                Start time
                </label>
                <input
                id="event-start"
                type="time"
                bind:value={startTime}
                required
                class="w-full rounded-lg border border-[#D9C9AE]
                        bg-white px-3 py-3"
                />
            </div>
            <div>
                <label for="event-end" class="mb-2 block text-sm font-medium">
                End time
                </label>
                <input
                id="event-end"
                type="time"
                bind:value={endTime}
                required
                class="w-full rounded-lg border border-[#D9C9AE]
                        bg-white px-3 py-3"
                />
            </div>
            </div>
        {/if}

        <div>
            <label for="event-category" class="mb-2 block text-sm font-medium">
            Category
            </label>
            <select
            id="event-category"
            bind:value={category}
            class="w-full rounded-lg border border-[#D9C9AE]
                    bg-white px-4 py-3"
            >
            {#each categories as item}
                <option value={item}>{item}</option>
            {/each}
            </select>
        </div>

        <div>
            <label for="event-description" class="mb-2 block text-sm font-medium">
            Notes (optional)
            </label>
            <textarea
            id="event-description"
            bind:value={description}
            rows="3"
            maxlength="2000"
            placeholder="Additional details..."
            class="w-full rounded-lg border border-[#D9C9AE]
                    bg-white px-4 py-3 outline-none
                    focus:border-[#8E2028]"
            ></textarea>
        </div>

        {#if error}
            <p role="alert" class="text-sm text-[#8E2028]">
            {error}
            </p>
        {/if}

        <div class="flex justify-end gap-3 pt-2">
            <button
            type="button"
            onclick={onCancel}
            class="rounded-lg border border-[#D9C9AE]
                    px-5 py-3 text-sm hover:bg-[#F5F0E6]"
            >
            Cancel
            </button>

            <button
            type="submit"
            class="rounded-lg bg-[#8E2028] px-6 py-3
                    text-sm font-semibold text-white
                    hover:bg-[#741920]"
            >
            {editingEvent ? 'Save Changes' : 'Create Event'}
            </button>
        </div>
        </form>
    </div>
    </div>