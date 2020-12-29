# The ELF Code
This is a web game that has multiple levels with progressive complexioty and to solve requires coding the avatar movements in javascript.

![Access](A-Elf-Code-access.png)

# Solution

## Level 1
```
elf.moveLeft(10)
elf.moveUp(10)
```

## Level 2
```
var ans = elf.get_lever(0) + 2
elf.moveLeft(6)
elf.pull_lever(ans)
elf.moveLeft(4)
elf.moveUp(10)
```

## Level 3
```
elf.moveTo(lollipop[0])
elf.moveTo(lollipop[1])
elf.moveTo(lollipop[2])
elf.moveUp(1)
```

## Level 4
```
for (var i = 0; i < 3; i++) {
  elf.moveLeft(3), elf.moveUp(11), elf.moveLeft(3), elf.moveDown(11)
}
```

## Level 5
```
elf.moveTo(lollipop[1])
elf.moveTo(lollipop[0])
var arr = elf.ask_munch(0)
var filtered = arr.filter(function(item) {
  return (parseInt(item) == item);
});
elf.tell_munch(filtered)
elf.moveUp(2)
```

## Level 6
```
var lev = elf.get_lever(0)
lev.unshift("munchkins rule")
for (var i = 0; i <= 3; i++) {
  elf.moveTo(lollipop[i]);
}
elf.moveTo(lever[0])
elf.pull_lever(lev)
elf.moveDown(3)
elf.moveLeft(6)
elf.moveUp(2)
```

## Level 7
Open the developer tools console and go to the `win_or_loose` function, add a break point, and enter the following commands before clicking play
```
this.game_grid[ this.cur_xy.y ][ this.cur_xy.x ]=4
this.lollipop_coords.length==0
```

## Level 8
