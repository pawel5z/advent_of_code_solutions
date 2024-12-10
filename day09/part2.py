from typing import List, Tuple, Optional


def disk_map_to_blocks(disk_map: str) -> List[str]:
    result = []
    for i, block_count in enumerate(map(int, disk_map)):
        if i % 2 == 0:
            result = result + block_count * [str(i // 2)]
        else:
            result = result + block_count * ['.']
    return result


def find_fitting_free_block_range(blocks: List[str], size: int, limit: int) -> Optional[Tuple[int, int]]:
    """_summary_

    Args:
        blocks (List[str]): _description_
        size (int): _description_
        limit (int): Free blocks range must not reach this.

    Returns:
        Optional[Tuple[int, int]]: _description_
    """
    free_blocks_begin = 0

    while free_blocks_begin < limit:

        while free_blocks_begin < limit and blocks[free_blocks_begin] != '.':
            free_blocks_begin += 1

        free_blocks_end = free_blocks_begin

        while free_blocks_end < limit and blocks[free_blocks_end] == '.':
            free_blocks_end += 1

        if free_blocks_end - free_blocks_begin >= size:
            return (free_blocks_begin, free_blocks_begin + size)

        free_blocks_begin = free_blocks_end

    return None


def rearrange(blocks: List[str]):
    file_blocks_end = len(blocks) - 1

    while file_blocks_end > 0:

        while file_blocks_end > 0 and blocks[file_blocks_end] == '.':
            file_blocks_end -= 1

        id = blocks[file_blocks_end]
        file_blocks_begin = file_blocks_end

        while file_blocks_begin >= 0 and blocks[file_blocks_begin] == id:
            file_blocks_begin -= 1

        free_block_range = find_fitting_free_block_range(
            blocks, file_blocks_end - file_blocks_begin, file_blocks_begin + 1)

        if free_block_range is None:
            file_blocks_end = file_blocks_begin
            continue

        blocks[free_block_range[0]:free_block_range[1]
               ] = blocks[file_blocks_begin + 1: file_blocks_end+1]
        blocks[file_blocks_begin + 1: file_blocks_end+1] = ['.'] * \
            len(blocks[file_blocks_begin + 1: file_blocks_end+1])


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
