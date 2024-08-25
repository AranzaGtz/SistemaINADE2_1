import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Alert } from "@/components/ui/alert";
import { AlertDescription, AlertTitle } from "@/components/ui/alert";

const TestPage: React.FC = () => {
  const [showAlert, setShowAlert] = useState(false);

  const handleClick = (bool: boolean) => {
    if (bool) {
      setShowAlert(true);
    } else {
      setShowAlert(false);
    }
  };

  return (
    <div className="flex h-screen items-center justify-center">
      <div>
        <h1 className="text-4xl font-bold text-red-300">Hello, World!</h1>
        <Button className="mt-4" onClick={() => handleClick(!showAlert)}>
          Click Me
        </Button>
        {showAlert && (
          <Alert>
            <AlertTitle>Heads up!</AlertTitle>
            <AlertDescription>
              You can add components and dependencies to your app using the cli.
            </AlertDescription>
          </Alert>
        )}
      </div>
    </div>
  );
};

export default TestPage;
