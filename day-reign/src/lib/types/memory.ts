export interface MemoryInput {
    title: string;
    date: string;
    content: string;
}

export interface Memory extends MemoryInput {
  id: string;
  createdAt: string;
  updatedAt: string;
}