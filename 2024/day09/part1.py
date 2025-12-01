from typing import List


def disk_map_to_blocks(disk_map: str) -> List[str]:
    result = []
    for i, block_count in enumerate(map(int, disk_map)):
        if i % 2 == 0:
            result = result + block_count * [str(i // 2)]
        else:
            result = result + block_count * ['.']
    return result


def rearrange(blocks: List[str]):
    free_block_index = 0
    file_block_index = len(blocks) - 1
    while free_block_index < file_block_index:
        while file_block_index > 0 and blocks[file_block_index] == '.':
            file_block_index -= 1
        while free_block_index < len(blocks) - 1 and blocks[free_block_index] != '.':
            free_block_index += 1
        if free_block_index >= file_block_index:
            return
        blocks[free_block_index] = blocks[file_block_index]
        blocks[file_block_index] = '.'


def checksum(blocks: List[str]) -> int:
    result = 0
    for i, id in enumerate(blocks):
        if id == '.':
            continue
        result += i * int(id)
    return result


def prettify_blocks(blocks: List[str]) -> str:
    return ''.join(blocks)


if __name__ == '__main__':
    disk_map = input()
    blocks = disk_map_to_blocks(disk_map)
    rearrange(blocks)
    print(checksum(blocks))
