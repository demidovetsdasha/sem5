package org.example.testomis.payload.request;

import jakarta.validation.constraints.NotBlank;
import lombok.Builder;
import org.example.testomis.model.enums.EventCategory;

@Builder
public record EventRequest(
        @NotBlank
        String name,

        @NotBlank
        String category,

        @NotBlank
        String author,

        @NotBlank
        String start,

        @NotBlank
        String finish
) {
}
