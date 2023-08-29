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
      <div className={"pt-5"}>
        {themes.map((theme, index) => (
          <div
            className={"mb-5 cursor-pointer"}
            key={theme.id}
            onClick={() => setThemeId(theme.id)}
          >
            <Button
              disabled={theme.viewed_video_amount <= 0}
              className={"p-0 small-button"}
              style={{
                borderColor: theme.viewed_video_amount > 0 ? color : "ffffff",
                color: theme.viewed_video_amount > 0 ? color : "ffffff",
                pointerEvents: "none",
              }}
              shape={"round"}
            >
              {theme.viewed_video_amount}/{theme.video_amount}
            </Button>
            <div className={"flex flex-row items-center"}>
              <TextBlock key={theme.id} bigText={theme.name} small_text={""} />
            </div>
            <Divider color={color} />
          </div>
        ))}
      </div>
    </Card>
  );
};

export default ThemeList;
