import { ulid } from "ulid";
import { IdGenerator } from "../id.generator.js";

export class UlidIdGenerator implements IdGenerator {
  get = (): Promise<string> => Promise.resolve(ulid());

  build = <U>(cb: (id: string) => U): Promise<U> => this.get().then(cb);
}
