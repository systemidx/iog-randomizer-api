using System;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Randomizer.Api.Models;

namespace Randomizer.Api.Extensions
{
    public static class FormFileExtensions
    {
        
        public static async Task<bool> IsValidRomFileAsync(this IFormFile rom)
        {
            using (var reader = new StreamReader(rom.OpenReadStream()))
            {
                const string HEADER = "\x49\x4C\x4C\x55\x53\x49\x4F\x4E\x20\x4F\x46\x20\x47\x41\x49\x41\x20\x55\x53\x41";
                var data = await reader.ReadToEndAsync();

                if (data.IndexOf(HEADER, StringComparison.Ordinal) == -1)
                    return false;
            }

            return true;
        }

        /// <summary>
        /// Returns the temporary storage location of the copied ROM file.
        /// </summary>
        /// <param name="rom"></param>
        /// <param name="cancellationToken"></param>
        /// <returns></returns>
        public static async Task<UploadedFileDetails> CopyFileToTempStorageAsync(this IFormFile rom, CancellationToken cancellationToken)
        {
            var directory = $@"{Path.GetTempPath()}\IOGR";
            if (!Directory.Exists(directory))
                Directory.CreateDirectory(directory);
            
            var name = DateTime.UtcNow.Ticks.ToString();
            var extension = Path.GetExtension(rom.FileName);

            var romPath = $@"{directory}\\{name}{extension}";

            using (var file = new FileStream(romPath, FileMode.Create))
            {
                file.Position = 0;
                await rom.CopyToAsync(file, cancellationToken);
            }

            return new UploadedFileDetails
            {
                Directory = directory,
                FileName = name,
                Extension = extension,
                FullPath = romPath
            };
        }
    }
}