import { createFileRoute } from "@tanstack/react-router";
import { Heading } from "@chakra-ui/react";

export const Route = createFileRoute("/")({
  component: Index,
});

function Index() {
  return (
    <Heading size="2xl" letterSpacing="tight">
      ApplyWise
    </Heading>
  );
}
