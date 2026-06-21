import { AppLayout } from "@/components/layout/AppLayout";
import { CommandRoomShell } from "@/components/command-room/CommandRoomShell";

export const metadata = {
  title: "Dealix · Command Room",
};

export default function CommandRoomPage() {
  return (
    <AppLayout>
      <CommandRoomShell />
    </AppLayout>
  );
}
