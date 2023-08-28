import React, { useEffect, useState } from "react";
import { useFetching } from "../hooks/useFetching";
import TextBlock from "./UI/TextBlock";
import ThemeService from "../services/ThemeService";
import Card from "./UI/Card";
import Divider from "./UI/Divider";
import { Button } from "antd";

const ThemeList = ({ courseChapterId, setThemeId, color }) => {
  const [themes, setThemes] = useState([]);
  const [fetchThemes, isLoading, error] = useFetching(async () => {
    const response = await ThemeService.get(courseChapterId);
    setThemes([...response.data]);
  });

  useEffect(() => {
    fetchThemes();
  }, [courseChapterId]);

  return (
    <Card text={"БЛОКИ ОБУЧЕНИЯ"}>
      {themes.map((theme, index) => (
        <div
          className={"mb-5 cursor-pointer"}
          key={theme.id}
          onClick={() => setThemeId(theme.id)}
        >
          <Button
            disabled={true}
            className={"p-0 small-button"}
            shape={"round"}
          >
            0/0
          </Button>
          <div className={"flex flex-row items-center"}>
            <TextBlock key={theme.id} bigText={theme.name} small_text={""} />
          </div>
          <Divider color={color} />
        </div>
      ))}
    </Card>
  );
};

export default ThemeList;
