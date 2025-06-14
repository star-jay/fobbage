export interface Answer {
  id: number;
  text: string;
}

export interface Question {
  id: number;
  question_text: string;
  answers: Answer[];
}

export interface Quiz {
  id: number;
  title: string;
  questions: Question[];
} 