import { create } from "zustand";
import { devtools, persist } from "zustand/middleware";

const useInterfaceStore = create(
  persist(
    devtools((set, get) => ({
      isOpenSettings: false,
      openCloseSettings: async () => {
        if (get().isOpenSettings) {
          set({ isOpenSettings: false });
        } else {
          set({ isOpenSettings: true });
        }
      },
    })),
    { name: "useUserStore" }
  )
);

export default useInterfaceStore;
