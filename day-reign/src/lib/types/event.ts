export type EventCategory = 
| 'Personal'
| 'School'
| 'Work'
| 'Health'
| 'Other';

export interface CalendarEvent {
    id: string;
    title: string;
    date: string;
    startTime: string;
    endTime: string;
    allDay: boolean;
    category: EventCategory;
    description: string;
}

export type EventInput = Omit<CalendarEvent, 'id'>;