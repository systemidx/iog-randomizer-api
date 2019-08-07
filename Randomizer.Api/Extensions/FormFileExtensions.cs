using System;
using System.IO;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Randomizer.Api.Configuration;
using Randomizer.Api.Models;

namespace Randomizer.Api.Extensions
{
    public static class FormFileExtensions
    {
        /// <summary>
        /// Returns whether or not the meets the criteria for validity.
        /// </summary>
        /// <param name="rom"></param>
        /// <returns></returns>
        public static bool IsValidRomFile(this IFormFile rom)
        {
            const string HEADER = "\x49\x4C\x4C\x55\x53\x49\x4F\x4E\x20\x4F\x46\x20\x47\x41\x49\x41\x20\x55\x53\x41";
            
            using (var reader = new BinaryReader(rom.OpenReadStream()))
            {
                try
                {
                    reader.BaseStream.Seek(0x00FFC0, SeekOrigin.Begin);
                    var bytes = reader.ReadBytes(20);
                    var data = Encoding.UTF8.GetString(bytes);

                    return string.Equals(data, HEADER, StringComparison.OrdinalIgnoreCase);
                }
                catch (IOException) { return false; }
                catch (ArgumentOutOfRangeException) { return false; }
            }
        }

        /// <summary>
        /// Returns the temporary storage location of the copied ROM file.
        /// </summary>
        /// <param name="rom"></param>
        /// <param name="cancellationToken"></param>
        /// <returns></returns>
        public static async Task<UploadedFileDetails> CopyFileToTempStorageAsync(this IFormFile rom, RandomizerConfiguration configuration, CancellationToken cancellationToken)
        {
            var name = DateTime.UtcNow.Ticks.ToString();
            var extension = Path.GetExtension(rom.FileName);

            var romPath = $@"{configuration.TempStorageDestination}\\{name}{extension}";

            using (var file = new FileStream(romPath, FileMode.Create))
            {
                file.Position = 0;
                await rom.CopyToAsync(file, cancellationToken);
            }

            return new UploadedFileDetails
            {
                Directory = configuration.TempStorageDestination,
                FileName = name,
                Extension = extension,
                FullPath = romPath
            };
        }
    }
}