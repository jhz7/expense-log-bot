export interface IdGenerator {
  get(): Promise<string>;
  build<U>(cb: (id: string) => U): Promise<U>;
}
