package main;
 
import (
    "github.com/fsnotify/fsnotify"
    "log"
    "fmt"
)
 
func main() {

    watch, err := fsnotify.NewWatcher();
    if err != nil {
        log.Fatal(err);
    }
    defer watch.Close();

    err = watch.Add("./tmp");
    if err != nil {
        log.Fatal(err);
    }

    go func() {
        for {
            select {
            case ev := <-watch.Events:
                {

                    if ev.Op&fsnotify.Create == fsnotify.Create {
                        log.Println("Create : ", ev.Name);
                    }
                    if ev.Op&fsnotify.Write == fsnotify.Write {
                        log.Println("Write : ", ev.Name);
                    }
                    if ev.Op&fsnotify.Remove == fsnotify.Remove {
                        log.Println("Remove : ", ev.Name);
                    }
                    if ev.Op&fsnotify.Rename == fsnotify.Rename {
                        log.Println("Rename : ", ev.Name);
                    }
                    if ev.Op&fsnotify.Chmod == fsnotify.Chmod {
                        log.Println("Chmod : ", ev.Name);
                    }
                }
            case err := <-watch.Errors:
                {
                    log.Println("error : ", err);
                    return;
                }
            }
        }
    }();
 
    select {};
}